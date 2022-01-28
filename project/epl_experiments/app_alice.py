from epl import epl_protocol_alice
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
    socket = Socket("alice","bob")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket]
    )



    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        
        # Create EPR Pair
        qubits = epr_socket.create(number=2)
        alice.flush()




        dm = get_qubit_state(qubits[0], reduced_dm=False)
        print(dm)
        storage = create_qubits(num_qubits=2)
        dm = DMState(storage,dm)

        fidelity = dm.fidelity(ketstates.b00)

        print("Starting fidelity Alice:" + str(fidelity)) 



        # Execute EPL Protocol
        result = epl_protocol_alice(qubits[0],qubits[1],alice,socket)
        print(result, "ALICE")
        alice.flush()




        dm = get_qubit_state(qubits[0], reduced_dm=False)
        storage = create_qubits(num_qubits=2)
        dm = DMState(storage,dm)

        fidelity = dm.fidelity(ketstates.b00)

        print("Ending fidelity Alice:" + str(fidelity)) 




        return result

if __name__ == "__main__":
    main()
