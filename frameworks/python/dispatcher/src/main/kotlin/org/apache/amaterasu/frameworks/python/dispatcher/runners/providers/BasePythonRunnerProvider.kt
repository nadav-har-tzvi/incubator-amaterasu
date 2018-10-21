package org.apache.amaterasu.frameworks.python.dispatcher.runners.providers

import org.apache.amaterasu.common.dataobjects.ActionData
import org.apache.amaterasu.sdk.frameworks.RunnerSetupProvider

abstract class BasePythonRunnerProvider : RunnerSetupProvider {
    override fun getCommand(jobId: String?, actionData: ActionData?, env: String?, executorId: String?, callbackAddress: String?): String {
        return "pip install -r requirements.txt"
    }

    override fun getRunnerResources(): Array<String> {
        return arrayOf("python_sdk.zip")
    }

    override fun getActionDependencies(jobId: String?, actionData: ActionData?): Array<String> {
        TODO("not implemented") //To change body of created functions use File | Settings | File Templates.
    }
}