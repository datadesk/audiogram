from os.path import expanduser
from fabric.api import env, task, run, local, cd, sudo


env.user = 'ubuntu'
env.project_dir = "/home/ubuntu/audiogram/"
env.hosts = ("audiogram.datadesk.news",)
env.key_filename = (expanduser('~/.ec2/datadesk.september.2017.pem'),)


@task
def pull():
    """
    Pull down the latest code from GitHub.
    """
    with cd(env.project_dir):
        run("git pull origin master")


@task
def restartnode():
    """
    Restart the node application.
    """
    with cd(env.project_dir):
        run("npm rebuild")
    run("pm2 restart server")


@task
def restartnginx():
    """
    Restart the Nginx web server.
    """
    sudo("service nginx restart")


@task
def deploy():
    """
    Deploy the latest code to production.
    """
    pull()
    restartnode()
    restartnginx()


@task
def ssh():
    """
    Log into the remote host using SSH
    """
    local("ssh {}@{} -i {}".format(
        env.user,
        env.hosts[0],
        env.key_filename[0]
    ))
