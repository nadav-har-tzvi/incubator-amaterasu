package org.apache.amaterasu.frameworks.python.dispatcher.runners.providers

import org.apache.amaterasu.common.configuration.ClusterConfig
import org.apache.amaterasu.common.dataobjects.ActionData

 class PandasRunnerProvider(env: String, conf: ClusterConfig): PythonRunnerProviderBase(env, conf) {
    override fun getActionUserResources(jobId: String, actionData: ActionData): Array<String> = arrayOf()

    override val runnerResources: Array<String>
        get() {
            var resources = super.runnerResources
            resources += "amaterasu_pandas-${conf.version()}.zip"
            return resources
        }

    override fun getCommand(jobId: String, actionData: ActionData, env: String, executorId: String, callbackAddress: String): String {
        return super.getCommand(jobId, actionData, env, executorId, callbackAddress) + " && $virtualPythonPath ${actionData.src}"
    }
}