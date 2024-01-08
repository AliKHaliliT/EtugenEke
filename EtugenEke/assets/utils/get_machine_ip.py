import platform
import subprocess
import os


class NetworkConfigFetcher:

    """
    
    This class is used to fetch the network configuration of the machine.
    It returns a list of dictionaries containing the interface alias, ip address and gateway, 
    for each interface that has an ip address and a gateway.
    
    """

    def __init__(self) -> None:

        """
        
        Constructor of the Network Config Fetcher class.


        Parameters
        ----------
        None.


        Returns
        -------
        None.

        """

        self.current_os = platform.system()


    def _parse_output(self, output: list[str]) -> list[dict[str, str]]:

        """
        
        Parses the output of the powershell and bash scripts.


        Parameters
        ----------
        output : list
            The output of the powershell or bash script.


        Returns
        -------
        parsed_output : list
            The cleaned output of the powershell or bash script.
            The output is a list of dictionaries containing the interface alias, ip address and gateway.
        
        """

        if not isinstance(output, list):
            raise TypeError(f"Invalid type: {type(output)}")
        for string in output:
            if not isinstance(string, str):
                raise TypeError(f"Invalid type: {type(string)}")
            

        parsed_output = []
        entry = {}
        for line in output:
            line = line.strip()
            if line.startswith("Interface"):
                entry["Interface"] = line.split(": ")[1]
            elif line.startswith("Address"):
                entry["Address"] = line.split(": ")[1]
            elif line.startswith("Gateway"):
                entry["Gateway"] = line.split(": ")[1]
                parsed_output.append(entry)
                entry = {}


        return parsed_output

    def _run_powershell_script(self) -> list[dict[str, str]]:

        """
        
        Runs the powershell script to fetch the network configuration.


        Parameters
        ----------
        None.


        Returns
        -------
        parsed_output : list
            The parsed output of the powershell script.
            The output is a list of dictionaries containing the interface alias, ip address and gateway.

        
        """

        ps_script = """
        $ntwk = Get-NetIPConfiguration

        foreach ($net in $ntwk) {
            if ($net.IPv4Address -ne $null -and $net.IPv4DefaultGateway -ne $null) {
                Write-Output "Interface: $($net.InterfaceAlias)"
                Write-Output "Address: $($net.IPv4Address.IPAddress)"
                Write-Output "Gateway: $($net.IPv4DefaultGateway.NextHop)"
                Write-Output ""
            }
        }
        """

        with open("network_config.ps1", "w") as ps_file:
            ps_file.write(ps_script)

        try:

            output = subprocess.check_output(["powershell.exe", "-File", "network_config.ps1"], stderr=subprocess.STDOUT)
            output = output.decode("utf-8").splitlines()
            cleaned_output = [line.strip("\r") for line in output if line.strip()]


            # Clean up
            os.remove("network_config.ps1")


            return self._parse_output(cleaned_output)
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"


    def _run_linux_script(self) -> list[dict[str, str]]:

        """
        
        Runs the bash script to fetch the network configuration.


        Parameters
        ----------
        None.


        Returns
        -------
        parsed_output : list
            The parsed output of the bash script.
            The output is a list of dictionaries containing the interface alias, ip address and gateway.
        
        """

        bash_script = """
        ntwk=$(ip -4 -o addr show)

        while IFS= read -r line; do
            interface_alias=$(echo "$line" | awk "{print $2}")
            ip_address=$(echo "$line" | awk "{print $4}")
            gateway=$(ip route | awk "/default/ {print $3}")

            if [[ -n $ip_address ]] && [[ -n $gateway ]]; then
                echo "Interface: $interface_alias"
                echo "Address: $ip_address"
                echo "Gateway: $gateway"
                echo ""
            fi
        done <<< "$ntwk"
        """

        with open("network_config.sh", "w") as bash_file:
            bash_file.write(bash_script)

        try:

            output = subprocess.check_output(["bash", "network_config.sh"], stderr=subprocess.STDOUT)
            output = output.decode("utf-8").splitlines()
            cleaned_output = [line.strip("\r") for line in output if line.strip()]


            # Clean up
            os.remove("network_config.sh")


            return self._parse_output(cleaned_output)
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"


    def fetch_network_config(self) -> list[dict[str, str]]:

        """

        Fetches the network configuration of the machine.


        Parameters
        ----------
        None.


        Returns
        -------
        network_config : list
            The parsed output of the powershell or bash script.
            The output is a list of dictionaries containing the interface alias, ip address and gateway.

        """

        if self.current_os == "Windows":
            return self._run_powershell_script()
        elif self.current_os == "Linux":
            return self._run_linux_script()
        else:
            raise OSError(f"Unsupported OS: {self.current_os}")