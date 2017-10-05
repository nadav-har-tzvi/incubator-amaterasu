<!--
  ~ Licensed to the Apache Software Foundation (ASF) under one or more
  ~ contributor license agreements.  See the NOTICE file distributed with
  ~ this work for additional information regarding copyright ownership.
  ~ The ASF licenses this file to You under the Apache License, Version 2.0
  ~ (the "License"); you may not use this file except in compliance with
  ~ the License.  You may obtain a copy of the License at
  ~
  ~      http://www.apache.org/licenses/LICENSE-2.0
  ~
  ~ Unless required by applicable law or agreed to in writing, software
  ~ distributed under the License is distributed on an "AS IS" BASIS,
  ~ WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  ~ See the License for the specific language governing permissions and
  ~ limitations under the License.
  -->
# Apache Amaterasu [![Build Status](https://travis-ci.org/apache/incubator-amaterasu.svg?branch=master)](https://travis-ci.org/apache/incubator-amaterasu)

                                               /\
                                              /  \ /\
                                             / /\ /  \
        _                 _                 / /  / /\ \   
       /_\   _ __   __ _ | |_  ___  _ _  __(_( _(_(_ )_) 
      / _ \ | '  \ / _` ||  _|/ -_)| '_|/ _` |(_-<| || |
     /_/ \_\|_|_|_|\__,_| \__|\___||_|  \__,_|/__/ \_,_|
                                                        

Apache Amaterasu is an open-source, deployment tool for data pipelines. Amaterasu allows developers to write and easily deploy data pipelines, and clusters manage their configuration and dependencies.

## Installation

In order to be able to install Apache Amaterasu and use it, please see that you have the following installed on the target machine:

* Java 1.8+
* libffi
* python3
* python3-devel

You will need [pip](https://pip.pypa.io/en/stable/installing/) installed on your machine.

Finally, to install Apache Amaterasu:

```
pip install amaterasu
```

> **Note** - Since we can't upload the Apache Amaterasu process JAR into PyPi, we only published the CLI itself.
When you install the CLI, it fetches the JAR from our server.

## Creating a dev/test Mesos cluster

We have also created a Mesos cluster you can use to test Amaterasu or use for development purposes.
For more details, visit the [amaterasu-vagrant](https://github.com/shintoio/amaterasu-vagrant) repo

## Running a Job

First, you need an Amaterasu-compatible git repository.
Our CLI offers the ability to generate a skeleton of an Apache Amaterasu compatible repository. And here is how:
```bash
cd <directory to designate as the Amaterasu repository>
ama init

# OR
ama init <relative or absolute path>

# e.g.
cd my-ama-repo
ama init

# OR
ama init my-ama-repo

# OR
ama init /home/myuser/somedir/someotherdir/my-ama-repo
```

Once you have the repository at hand, upload it to a remote host (e.g. - github)


Finally, to run the job:
```
ama run <repository_url>

# e.g.

ama run https://github.com/shintoio/amaterasu-job-sample.git

# By default , we use the master branch, but if you want another branch:

ama run <repository_url> -b <your_branch>

# e.g.

ama run https://github.com/shintoio/amaterasu-job-sample.git -b python-support

# We also support different environments, we use the "default" environment by default.
# To use another environment:
ama run <repository_url> -e <environment>

# e.g. 
ama run https://github.com/shintoio/amaterasu-job-sample.git -e test
```
For more CLI options, use the builtin help (ama help)

It is highly recommended that you take a peek at our [sample job repository](https://github.com/shintoio/amaterasu-job-sample.git) before using Amaterasu.


# Apache Amaterasu Developers Information 

## Building Apache Amaterasu

to build the amaterasu home dir (for dev purposes) run:
```
./gradlew buildHomeDir test
```

to create a distributable jar (clean creates the home dir first) run:
```
./gradlew buildDistribution test
```

## Architecture

Amaterasu is an Apache Mesos framework with two levels of schedulers:

* The ClusterScheduler manages the execution of all the jobs
* The JobScheduler manages the flow of a job

The main clases in Amateraso are listed bellow:

    +-------------------------+   +------------------------+
    | ClusterScheduler        |   | Kami                   |
    |                         |-->|                        |
    | Manage jobs:            |   | Manages the jobs queue |
    | Queue new jobs          |   | and Amaterasu cluster  |
    | Reload interrupted jobs |   +------------------------+
    | Monitor cluster state   |
    +-------------------------+
                |
                |     +------------------------+
                |     | JobExecutor            |
                |     |                        |
                +---->| Runs the Job Scheduler |
                      | Communicates with the  |
                      | ClusterScheduler       |
                      +------------------------+
                                 |
                                 |
                      +------------------------+      +---------------------------+                      
                      | JobScheduler           |      | JobParser                 |
                      |                        |      |                           |
                      | Manages the execution  |----->| Parses the kami.yaml file |
                      | of the job, by getting |      | and create a JobManager   |
                      | the  execution flow    |      +---------------------------+
                      | fron the JobManager    |                    |
                      | and comunicating with  |      +---------------------------+
                      | Mesos                  |      | JobManager                |                      
                      +------------------------+      |                           |
                                 |                    | Manages the jobs workflow |
                                 |                    | independently of mesos    |
                      +------------------------+      +---------------------------+
                      | ActionExecutor         |
                      |                        |
                      | Executes ActionRunners |
                      | and manages state for  |
                      | the executor           |
                      +------------------------+

                      

