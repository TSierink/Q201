from epl import epl_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
from netsquid.qubits import ketstates, ket2dm
from netqasm.sdk.external import get_qubit_state
from netqasm.sdk.toolbox.sim_states import get_fidelity, to_dm, qubit_from

from netsquid.qubits.dmtools import DMState
from netsquid.qubits.kettools import KetState
from netsquid.qubits.qubitapi import create_qubits, assign_qstate




def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice","bob")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket],
        max_qubits = 100
    )



    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:

        old_pair = epr_socket.create(number=1)
        alice.flush()

        dm = get_qubit_state(old_pair[0], reduced_dm=False)

        if(dm.shape == (4,4)):
            # Prepare storage for comparing
            storage = create_qubits(num_qubits=2)
            # Place the state of the combined pair into the storage
            dm = DMState(storage,dm)

            # Compare with the desired EPR pair
            fidelity = dm.fidelity(ketstates.b00)

            print("Base fidelity:" + str(fidelity)) 


        fidelity = 0
        good_pairs = []

        for i in range(12):
            # Create EPR Pairs
            qubits = epr_socket.create(number=2)
            alice.flush()

            # Execute EPL Protocol
            result = epl_protocol_alice(qubits[0],qubits[1],alice,socket)
            alice.flush()

            # Get dm representation of both qubits (not reduced)
            dm = get_qubit_state(qubits[0], reduced_dm=False)
            if(dm.shape == (4,4)):
                # Prepare storage for comparing
                storage = create_qubits(num_qubits=2)
                # Place the state of the combined pair into the storage
                dm = DMState(storage,dm)

                # Compare with the desired EPR pair
                fidelity = dm.fidelity(ketstates.b00)

                #print("Fidelity old_pair: " + str(fidelity)) 

            print("Round " + str(i), result, fidelity)

            if(result == True):
                good_pairs.append(qubits[0])

        print("PHASE 2")
        for i in range(0,len(good_pairs)-1,2):
            # Execute EPL Protocol
            result = epl_protocol_alice(good_pairs[i],good_pairs[i+1],alice,socket)
            #print(result, "ALICE")
            alice.flush()

            # Get dm representation of both qubits (not reduced)
            dm = get_qubit_state(good_pairs[i], reduced_dm=False)
            if(dm.shape == (4,4)):
                # Prepare storage for comparing
                storage = create_qubits(num_qubits=2)
                # Place the state of the combined pair into the storage
                dm = DMState(storage,dm)

                # Compare with the desired EPR pair
                fidelity = dm.fidelity(ketstates.b00)

            print("Round " + str(i), result, fidelity)


        return result

if __name__ == "__main__":
    main()
