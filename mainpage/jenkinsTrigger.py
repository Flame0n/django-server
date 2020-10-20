import jenkins
import time

JENKINS_URL = "http://3.137.149.140:8080"
JENKINS_USERNAME = "admin"
JENKINS_PASSWORD = "admin"


class JenkinsTrigger:
    def __init__(self):
        self.jenkins_server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)
        user = self.jenkins_server.get_whoami()
        version = self.jenkins_server.get_version()
        print ("Jenkins Version: {}".format(version))
        print ("Jenkins User: {}".format(user['id']))

    async def build_job(self, name, parameters=None, token=None):
        next_build_number = self.jenkins_server.get_job_info(name)['nextBuildNumber']
        self.jenkins_server.build_job(name, parameters=parameters, token=token)
        time.sleep(15)
        return self.jenkins_server.get_build_info(name, next_build_number)

    
