from epl import epl_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netsquid.qubits import ketstates, ket2dm
from netqasm.sdk.external import get_qubit_state
from netqasm.sdk.toolbox.sim_states import get_fidelity, to_dm, qubit_from

from netsquid.qubits.dmtools import DMState
from netsquid.qubits.kettools import KetState
from netsquid.qubits.qubitapi import create_qubits

def main(app_config=None):
    
    # Create a socket for classical communication
    socket = Socket("bob","alice")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Alice's NetQASM connection
    bob = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket],
        max_qubits = 1000
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's EPL method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        old_pair = epr_socket.recv(number=1)
        bob.flush()

        old_pair[0].free()

        while(True):
            # Create EPR Pairs
            qubits = epr_socket.recv(number=4)
            bob.flush()

            # Execute EPL Protocol
            result1 = epl_protocol_bob(qubits[0],qubits[1],bob,socket)
            bob.flush()

            result2 = epl_protocol_bob(qubits[2],qubits[3],bob,socket)
            bob.flush()

            if(result1 and result2):
                dm1 = get_qubit_state(qubits[0], reduced_dm=False)
                dm2 = get_qubit_state(qubits[2], reduced_dm=False)

                result3 = epl_protocol_bob(qubits[0],qubits[2],bob,socket)
                bob.flush()

                dm = get_qubit_state(qubits[0], reduced_dm=False)

                qubits[0].free()
                if(result3 and dm.shape==(4,4) and dm1.shape==(4,4) and dm2.shape==(4,4)):
                    break
            else:
                qubits[0].free()
                qubits[2].free()

            bob.flush()
        return True


if __name__ == "__main__":
    main()
