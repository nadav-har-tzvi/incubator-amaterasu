package org.apache.amaterasu.frameworks.python.dispatcher

import org.apache.amaterasu.common.configuration.enums.ActionStatus
import org.apache.amaterasu.common.dataobjects.ActionData
import org.apache.amaterasu.frameworks.python.dispatcher.runners.providers.PythonRunnerProvider
import org.jetbrains.spek.api.Spek
import org.jetbrains.spek.api.dsl.given
import org.jetbrains.spek.api.dsl.it
import org.jetbrains.spek.api.dsl.on
import org.junit.platform.runner.JUnitPlatform
import org.junit.runner.RunWith
import kotlin.test.assertEquals
import kotlin.test.assertNotEquals
import kotlin.test.assertNotNull

@RunWith(JUnitPlatform::class)
class PythonRunnerProviderTests: Spek({

    given("A python runner provider") {
        val runner = PythonRunnerProvider()
        on("Asking to run a simple python script with dummy actionData") {
            val command = runner.getCommand("AAAA",
                    ActionData(ActionStatus.pending(),
                            "AAA",
                            "AAA",
                            "AAA",
                            "AAA",
                            "AAA",
                            null,
                            null),
                    "",
                    "",
                    "")
            it("should yield a command") {
                assertNotNull(command)
            }
            it("should yield a non empty command") {
                assertNotEquals("", command)
            }

        }
        on("asking to run a simple python script with dependencies") {
            val actionData = ActionData(ActionStatus.queued(), "Simple Python", "simple.py", "python", "python", "Test", null, null)
            val command = runner.getCommand("Test", actionData, "", "", "")
            it("Should yield command that runs simple.py") {
                assertEquals("pip install -r requirements.txt && python simple.py", command)
            }
        }
    }


})