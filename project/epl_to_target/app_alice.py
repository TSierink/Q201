from epl import epl_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netsquid.qubits import ketstates, ket2dm
from netqasm.sdk.external import get_qubit_state
from netqasm.sdk.toolbox.sim_states import get_fidelity, to_dm, qubit_from

from netsquid.qubits.dmtools import DMState
from netsquid.qubits.kettools import KetState
from netsquid.qubits.qubitapi import create_qubits, assign_qstate

import time



def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice","bob")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket],
        max_qubits = 1000
    )



    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:

        old_pair = epr_socket.create(number=1)
        alice.flush()

        print("Base fidelity: ", get_fidelity(old_pair)) 

        old_pair[0].free()

        while(True):
            # Create EPR Pairs
            qubits = epr_socket.create(number=4)
            alice.flush()

            # Execute EPL Protocol
            result1 = epl_protocol_alice(qubits[0],qubits[1],alice,socket)
            alice.flush()

            result2 = epl_protocol_alice(qubits[2],qubits[3],alice,socket)
            alice.flush()

            print(result1, result2, get_fidelity(qubits[0]), get_fidelity(qubits[2]))

            if(result1 and result2):
                dm1 = get_qubit_state(qubits[0], reduced_dm=False)
                dm2 = get_qubit_state(qubits[2], reduced_dm=False)
                print(dm1.shape)                
                print(dm2.shape)   

                result3 = epl_protocol_alice(qubits[0],qubits[2],alice,socket)
                alice.flush()

                print(result3, get_fidelity(qubits[0]))

                dm = get_qubit_state(qubits[0], reduced_dm=False)

                qubits[0].free()
                if(result3 and dm.shape==(4,4) and dm1.shape==(4,4) and dm2.shape==(4,4)):
                    break
            else:
                qubits[0].free()
                qubits[2].free()

            alice.flush()
        return True



def get_fidelity(qubit):
    fidelity = 0
    # Get dm representation of both qubits (not reduced)
    dm = get_qubit_state(qubit, reduced_dm=False)
    if(dm.shape == (4,4)):
        # Prepare storage for comparing
        storage = create_qubits(num_qubits=2)
        # Place the state of the combined pair into the storage
        dm = DMState(storage,dm)

        # Compare with the desired EPR pair
        fidelity = dm.fidelity(ketstates.b00)
    return fidelity
    


if __name__ == "__main__":
    main()
