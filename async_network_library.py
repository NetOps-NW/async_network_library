
import asyncio, asyncssh;

class async_ssh_library:
    def __init__(self, device_details_dict):
        self.device_details_dict = device_details_dict;
        self.connection = None;
        self.process = None;
        self.sequence_of_default_prompts = set();

    async def __aenter__(self):
        if self.device_details_dict["jdict"]:
            jconnection = await asyncssh.connect(**self.device_details_dict["jdict"]);
            self.connection = await jconnection.connect_ssh(**self.device_details_dict["rdict"]);
        else:
            self.connection = await asyncssh.connect(**self.device_details_dict["rdict"]);

        self.process = await self.connection.create_process(stderr=asyncssh.STDOUT);
        await asyncio.sleep(1);
        self.sequence_of_default_prompts.add((await self.process.stdout.read(8192)).split("\n")[-1]);
        self.process.stdin.write("\n");
        return self;

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        if self.process and isinstance(self.process, asyncssh.SSHClientProcess):
            self.process.close();
        if self.connection and isinstance(self.connection, asyncssh.SSHClientConnection):
            self.connection.close();

    async def exec_specific_command(self, command=str(), return_str=str(), timeout=3600): 
        if len(command.split(":")) != 3:
            self.process.stdin.write(command.split(":")[0].strip() + "\n");
            for delay in range(timeout):
                await asyncio.sleep(1);
                try:
                    return_str += await asyncio.wait_for(self.process.stdout.read(8192), 2);
                except asyncio.exceptions.TimeoutError:
                    raise Exception(f"Command \"{command.split(':')[0].strip()}\" is not finished yet.");
                for prompt in self.sequence_of_default_prompts:
                    if prompt in return_str.split("\n")[-1]:
                        return return_str;
            else:
                raise Exception(f"Command \"{command.split(':')[0].strip()}\" is not finished yet.");
        else:
            self.process.stdin.write(command.split(":")[0].strip() + "\n");
            for delay in range(int(command.split(":")[2].strip())):
                await asyncio.sleep(1);
                try:
                    return_str += await asyncio.wait_for(self.process.stdout.read(8192), 2);
                except asyncio.exceptions.TimeoutError:
                    raise Exception(f"Command \"{command.split(':')[0].strip()}\" is not finished yet.");
                if command.split(":")[1].strip() in return_str.split("\n")[-1]:
                    self.sequence_of_default_prompts.add(return_str.split("\n")[-1]);
                    return return_str;
            else:
                raise Exception(f"Command \"{command.split(':')[0].strip()}\" is not finished yet.");

class async_scp_library:
    def __init__(self, device_details_dict):
        self.device_details_dict = device_details_dict;
        self.connection = None;

    async def __aenter__(self):
        if self.device_details_dict["jdict"]:
            jconnection = await asyncssh.connect(**self.device_details_dict["jdict"]);
            self.connection = await jconnection.connect_ssh(**self.device_details_dict["rdict"]);
        else:
            self.connection = await asyncssh.connect(**self.device_details_dict["rdict"]);
        return self;

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        if self.connection and isinstance(self.connection, asyncssh.SSHClientConnection):
            self.connection.close();

    async def copy_path_to_server(self, local_path, remote_path, recurse=False):
        await asyncssh.scp(local_path, (self.connection, remote_path), recurse=True if recurse else False);

    async def copy_path_from_server(self, remote_path, local_path, recurse=False):
        await asyncssh.scp((self.connection, remote_path), local_path, recurse=True if recurse else False);

