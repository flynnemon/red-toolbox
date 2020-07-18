
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version
from kubernetes import client, config
from colorama import Fore, Back, Style 
import base64, json

VERSION_BANNER = """
Manage Kubernetes secrets %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Manage Kubernetes secrets'

        # text displayed at the bottom of --help output
        epilog = 'Usage: kubesecret command1 --foo bar'

        # controller level arguments. ex: 'kubesecret --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        help='Read Kubernetes secrets',

        arguments=[
            ( [ '-d', '--decrypt' ],
              { 'help' : 'show secret values in plain text',
                'action'  : 'store_true',
                'dest' : 'decrypt',
                'default' : False } ),
            ( [ '-n', '--namespace' ],
              { 'help' : 'Kubernetes namespace to look for secrets',
                'action'  : 'store',
                'dest' : 'namespace',
                'default' : 'default' } ),
            ( [ '-s', '--secret' ],
              { 'help' : 'Read a specific secret by name',
                'action'  : 'store',
                'dest' : 'secret',
                'default' : None } )
        ],
    )
    def read(self):
        """Read Kubernetes secrets."""
        config.load_kube_config()
        v1 = client.CoreV1Api()
        if self.app.pargs.secret == None:
            ret = v1.list_namespaced_secret(self.app.pargs.namespace, pretty=True)
            for i in ret.items:
                print(Fore.GREEN + i.metadata.name + Style.RESET_ALL + " :") 
                for key, value in i.data.items():
                    if self.app.pargs.decrypt == False:
                        print("  {0}".format(key))
                    else:
                        print("  {0} : {2}{1}{3}".format(key, base64.b64decode(value).decode('UTF-8'), Style.DIM, Style.RESET_ALL))
                print("")
        else:
            ret = v1.read_namespaced_secret('sirena', self.app.pargs.namespace)
            print(Fore.GREEN + ret.metadata.name + Style.RESET_ALL + " :") 
            for key, value in ret.data.items():
                if self.app.pargs.decrypt == False:
                    print("  {0}".format(key))
                else:
                    print("  {0} : {2}{1}{3}".format(key, base64.b64decode(value).decode('UTF-8'), Style.DIM, Style.RESET_ALL))
            print("")


    @ex(
        help='Write Kubernetes secrets',

        arguments=[
            ( [ '-n', '--namespace' ],
              { 'help' : 'Kubernetes namespace to store secrets',
                'action'  : 'store',
                'dest' : 'namespace',
                'default' : 'default' } ),
            ( [ '-s', '--secret' ],
              { 'help' : 'Read a specific secret by name',
                'action'  : 'store',
                'dest' : 'secret',
                'default' : None } ),
            ( [ '-d', '--data' ],
              { 'help' : 'Data to add to the secret',
                'action'  : 'store',
                'dest' : 'data' } )
        ],
    )
    def write(self):
        """Write Kubernetes secrets."""

        config.load_kube_config()
        v1 = client.CoreV1Api()
        body = {
            "data": {},
            "metadata": {
                "name": self.app.pargs.secret
            }
        }

        data = self.app.pargs.data.split(',')
        print(data)
        for x in data:
            body['data'][x.split('=')[0]] = base64.b64encode(str.encode(x.split('=')[1])).decode('UTF-8')
        print(body)

        try:
            ret = v1.create_namespaced_secret(self.app.pargs.namespace, body)
            print(ret)
        except client.rest.ApiException as e:
            e = json.loads(e.body)
            print(e)
            if e['code'] == 409:
                self.app.log.warning('Secret already exists, appending data to existing secret.')
                try:
                    ret = v1.patch_namespaced_secret(self.app.pargs.secret, self.app.pargs.namespace, body)
                    self.app.log.debug(ret)
                except client.rest.ApiException as e:
                    print("Exception when calling CoreV1Api->patch_namespaced_secret: %s\n" % e)