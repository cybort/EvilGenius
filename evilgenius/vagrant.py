import os
import subprocess

from distutils.spawn import find_executable

class NetworkTopology(object):
    """
    This class shall be used to store the topology of the network.
    """
    
    @property
    def router(self):
        """
        Returns:
            :class:`evilgenius.vagrant.VagrantBox` 

            the router to be used for this given network topology.
        """
        pass

class VagrantFile(object):
    def __init__(self, boxes, network):
        """
        Args:
            
            boxes (list): a list of :class:`evilgenius.vagrant.VagrantBox` instances.

            network (:class:`evilgenius.vagrant.NetworkTopology`): the network
                topology for the given Vagrantfile.
        """
        pass
    
    @property
    def content(self):
        """
        Returns:
            string.

                the content of the Vagrantfile.
        """
        pass

class VagrantBox(object):
    def __init__(self, name, box="precise32", install_scripts=[]):
        self.name = name
        self.box = box
        if not type(install_scripts) is list:
            install_scripts = [install_scripts]
        self.install_scripts = install_scripts

    @property
    def definition(self):
        provision_lines = ""

        for script in self.install_scripts:
            provision_lines += """
            probe.vm.provision :shell, :inline => "{script}"
            """.format(script=script)

        code = """
        config.vm.define :{name} do |{name}|
            probe.vm.box = "{box}"
            probe.vm.provider :virtualbox do |vb|
              vb.customize ["modifyvm", :id, "--nic2", "intnet"]
              vb.customize ["modifyvm", :id, "--intnet2", "probe"]
            end
            {provision_lines}
        end
        """.format(box=self.box, name=self.name, provision_lines=provision_lines)
        return code

class VagrantController(object):
    def __init__(self, root=None):
        if not root:
            root = os.getcwd()
        self.root = root
        self.vagrant_executable = find_executable('vagrant')
        if not self.vagrant_executable:
            print "[!] Vagrant does not appear to be installed."
            print "    Please download and install a copy of it here:"
            print "    http://downloads.vagrantup.com/"
            sys.exit(1)

    def create_box(self, box):
        """
        Creates a new Vagrant box. If the box already exists it will raise an
        error.

        Args:

            box (:class:`evilgenius.vagrant.VagrantBox`): the vagrant box to be
                created. Will generate the appropriate VagrantFile for the
                specified box and initialize the box.
        """
        pass

    def init(self, vm=None):
        args = ['init']
        if vm:
            args += vm
        self._vagrant(args)

    def up(self, vm=None):
        args = ['up']
        if vm:
            args += vm
        self._vagrant(args)

    def destroy(self, vm=None):
        args = ['destroy']
        if vm:
            args += vm
        self._vagrant(args)

    def _vagrant(self, command):
        args = [self.vagrant_executable] + command
        p = subprocess.Popen(args, shell=True, cwd=self.root,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,
        retval = p.wait()