from unittest import TestCase, mock
from amaterasu.cli.handlers.run import RunPipelineHandler
from hamcrest import *
from string import Template
import netifaces


ama_props_tpl = Template("""zk=$zk

master=$master

user=root

webserver.port=8000

webserver.root=dist

spark.version=2.1.1-bin-hadoop2.7""")


class TestAmaterasuPropertiesGeneration(TestCase):

    def test_amaterasu_properties_with_valid_gateway_zk_master_ip_should_be_loopback(self):
        with mock.patch.object(netifaces, "gateways", return_value={'default': {}}), \
             mock.patch('builtins.open', mock.mock_open()) as w:
            expected = ama_props_tpl.substitute(zk='127.0.0.1', master='127.0.0.1')
            handler = RunPipelineHandler(None)
            handler._generate_amaterasu_properties()
            handle = w()
            handle.write.assert_called_once_with(expected)

    def test_amaterasu_properties_with_valid_gateway_zk_master_ip_should_be_192_168_0_1(self):
        with mock.patch.object(netifaces, 'gateways', return_value={"default": {netifaces.AF_INET: [0, "eth0"]}}), \
             mock.patch.object(netifaces, "ifaddresses", return_value={netifaces.AF_INET: [{'addr': '192.168.0.1'}]}), \
             mock.patch('builtins.open', mock.mock_open()) as w:
            expected = ama_props_tpl.substitute(zk='192.168.0.1', master='192.168.0.1')
            handler = RunPipelineHandler(None)
            handler._generate_amaterasu_properties()
            handle = w()
            handle.write.assert_called_once_with(expected)

