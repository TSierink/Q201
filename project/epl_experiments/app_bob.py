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
        epr_sockets = [epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's EPL method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        
        # Receive half of epr pairs
        qubits = epr_socket.recv(number=2)
        bob.flush()



        dm = get_qubit_state(qubits[0], reduced_dm=False)
        storage = create_qubits(num_qubits=2)
        print(dm)
        dm = DMState(storage,dm)

        fidelity = dm.fidelity(ketstates.b00)

        print("Starting fidelity Bob:" + str(fidelity)) 


        
        # Execute EPL Protocol
        result = epl_protocol_bob(qubits[0],qubits[1],bob,socket)
        print(result, "BOB")
        bob.flush()




        dm = get_qubit_state(qubits[0], reduced_dm=False)
        storage = create_qubits(num_qubits=2)
        dm = DMState(storage,dm)

        fidelity = dm.fidelity(ketstates.b00)

        print("Ending fidelity Bob:" + str(fidelity)) 


        return result

if __name__ == "__main__":
    main()
