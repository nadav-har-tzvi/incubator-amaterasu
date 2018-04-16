"""
Create or change Amaterasu's configuration.

Usage:
    ama config ( mesos | yarn )

"""
import netifaces
from string import Template

from .base import BaseHandler
import os
import abc
import socket
import getpass


def get_current_ip():
    default_gateway = netifaces.gateways()['default']
    if default_gateway:
        netface_name = default_gateway[netifaces.AF_INET][1]
        ip = netifaces.ifaddresses(netface_name)[netifaces.AF_INET][0][
            'addr']
    else:
        ip = '127.0.0.1'
    return ip


class ValidationError(Exception):
    pass


class ConfigurationField(metaclass=abc.ABCMeta):

    def __init__(self, required=False, input_text=None, default=None, name=None) -> None:
        self.required = required
        self.input_text = input_text
        self._default = default
        self.name = name

    def clean(self, value):
        if not value and value != 0 and self._default is not None:
            return self.default
        if self.required and value is None:
            raise ValidationError('This field is required')
        return value

    @property
    def default(self):
        if callable(self._default):
            value = self._default()
        else:
            value = self._default
        return value


class TextField(ConfigurationField):

    def clean(self, value):
        cleaned_value = super().clean(value)
        if str not in type(cleaned_value).mro():
            return str(cleaned_value)
        else:
            return cleaned_value


class NumericField(ConfigurationField):

    def clean(self, value):
        cleaned_value = super().clean(value)
        if int not in type(cleaned_value).mro() and float not in type(cleaned_value).mro():
            try:
                int_val = int(cleaned_value)
                float_val = float(cleaned_value)
                if int_val != float_val:
                    return float_val
                else:
                    return int_val
            except:
                raise ValidationError("Value must be a number")
        else:
            return cleaned_value


class IPField(TextField):

    def clean(self, value):
        cleaned_value = super().clean(value)
        try:
            socket.inet_aton(cleaned_value)
            return cleaned_value
        except:
            raise ValidationError('Value must be a valid IP address')


class ConfigurationMeta(abc.ABCMeta):

    @staticmethod
    def find_fields_for_cls(fields):
        vars_map = {}
        for var, value in fields.items():
            if ConfigurationField in value.__class__.mro():
                vars_map[var] = value
        return vars_map

    def __new__(mcls, name, bases, namespace, **kwargs):
        vars_map = {}
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        vars_map.update(ConfigurationMeta.find_fields_for_cls(vars(cls)))
        for base in bases:
            vars_map.update(ConfigurationMeta.find_fields_for_cls(vars(base).get('_fields', {})))
        setattr(cls, '_fields', vars_map)
        for var in vars_map:
            setattr(cls, var, None)
        return cls


class BaseConfigurationHandler(BaseHandler, metaclass=ConfigurationMeta):

    platform = None
    zk = IPField(required=True, input_text='Zookeeper IP', default=get_current_ip)
    master = IPField(required=True, input_text='Mesos master IP', default=get_current_ip)
    user = TextField(required=True, default=getpass.getuser())
    spark_version = TextField(default='2.1.1-bin-hadoop2.7',
                              input_text='Spark version', name='spark.version')

    def _get_user_input_for_field(self, var_name: str, field: ConfigurationField):
        input_tpl = Template('$input_text $default:')
        valid = False
        while not valid:
            if field.input_text:
                input_string = Template(input_tpl.safe_substitute(input_text=field.input_text))
            else:
                input_string = Template(input_tpl.safe_substitute(input_text=var_name))
            if field.default:
                input_string = input_string.safe_substitute(
                    default='[{}]'.format(field.default))
            else:
                input_string = input_string.safe_substitute(default='')
            value = input(input_string)
            try:
                field.clean(value)
                valid = True
            except ValidationError as e:
                print('{}. Please try again'.format(e))

    def _collect_user_input(self):
        for var_name, field in self._fields.items():
            value = self._get_user_input_for_field(var_name, field)
            setattr(self, var_name, value)

    def _render_properties_file(self):
        field_tpl = '{var}={value}\n'
        os.makedirs(os.path.expanduser('~/.amaterasu'), exist_ok=True)
        with open(os.path.expanduser('~/.amaterasu/amaterasu.properties'), 'w') as f:
            f.write(field_tpl.format(var='platform', value=self.platform))
            for var_name in self._fields.keys():
                f.write(field_tpl.format(var=var_name, value=getattr(self, var_name)))

    def handle(self):
        self._collect_user_input()
        self._render_properties_file()


class MesosConfigurationHandler(BaseConfigurationHandler):

    amaterasu_port = NumericField(default=8000, input_text='Amaterasu server port', name='webserver.port')
    amaterasu_root = TextField(default='dist', input_text='Amaterasu server root path', name='amaterasu.root')
    platform = 'mesos'


class YarnConfigurationHandler(BaseConfigurationHandler):

    yarn_queue = TextField(default='default', input_text='YARN queue name', name='yarn.queue')
    yarn_jarspath = TextField(default='hdfs:///apps/amaterasu', name='yarn.jarspath')
    spark_home = TextField(default='/usr/hdp/current/spark2-client', name='spark.home')
    yarn_homedir = TextField(default='/etc/hadoop', name='yarn.hadoop.home.dir')
    spark_yarn_java_opts = TextField(default='-Dhdp.version=2.6.1.0-129', name='spark.opts.spark.yarn.am.extraJavaOptions')
    spark_driver_java_opts = TextField(default='-Dhdp.version=2.6.1.0-129', name='spark.opts.spark.driver.extraJavaOptions')
    platform = 'yarn'


def get_handler(**kwargs):
    if kwargs['mesos']:
        return MesosConfigurationHandler
    elif kwargs['yarn']:
        return YarnConfigurationHandler
    else:
        raise ValueError('Could not find a handler for the given arguments')