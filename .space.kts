
job("Build & Deploy Python Implementations") {

    startOn {
        gitPush {
            anyBranchMatching {
                +"release-*"
                +"master"
                +"main"
            }
        }
    }

    parameters {
      text("CURRENT_MONTH", value = "$(date +'%m')")
      text("VERSION_NUMBER", value = "${"$"}CURRENT_YEAR.${"$"}CURRENT_MONTH.${"$"}JB_SPACE_EXECUTION_NUMBER")
    }

   // To check a condition, basically, you need a kotlinScript step
    host(displayName = "Setup Version") {
        kotlinScript { api ->
            // To pass the result of the condition to other steps, create a job parameter
            api.parameters["CURRENT_YEAR"] = LocalDateTime.now()
        }
    }


    host("Build Python Implementations Images") {
        dockerBuildPush {
            // by default, the step runs not only 'docker build' but also 'docker push'
            // to disable pushing, add the following line:
            // push = false

            // path to Docker context (by default, context is working dir)
            // context = "docker"
            // path to Dockerfile relative to the project root
            // if 'file' is not specified, Docker will look for it in 'context'/Dockerfile
            file = "Dockerfile"
            // build-time variables
            // args["HTTP_PROXY"] = "http://10.20.30.2:1234"
            // image labels
            // labels["vendor"] = "mycompany"
            // to add a raw list of additional build arguments, use
            // extraArgsForBuildCommand = listOf("...")
            // to add a raw list of additional push arguments, use
            // extraArgsForPushCommand = listOf("...")
            // image tags
            tags {
                // use current job run number as a tag - '0.0.run_number'
                +"50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/eapp-python-implementations:${"$"}VERSION_NUMBER"
            }
        }
    }
    
    host("Deploy Python Implementations Containers") {

      shellScript {
        content = """
          docker stop eapp-identity-services  # Stop the existing container
          docker rm eapp-identity-services    # Remove the stopped container
          docker run -d --restart=always -p 5000:80 --name eapp-python-implementations \
            50gramx.registry.jetbrains.space/p/main/ethosindiacontainers/eapp-python-implementations:1.0.${"$"}JB_SPACE_EXECUTION_NUMBER
        """
      }
    }
    
    // run this job only on
    // a Windows worker
    // that is tagged as 'pool-1'
    requirements {
        workerTags("windows-pool")
    }
}