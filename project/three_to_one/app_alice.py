from three_to_one import three_to_one_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import get_fidelity, to_dm, qubit_from
from netqasm.util.states import bloch_sphere_rep
import numpy

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

    # Create Alice's context, initialize EPR pairs inside it and call Alice's 3->1 method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        
        # Create EPR Pair
        qubits = epr_socket.create(number=3)
        alice.flush()

        # Save state of original qubits
        a0_state = get_qubit_state(qubits[0])
        a1_state = get_qubit_state(qubits[1])
        a2_original_state = get_qubit_state(qubits[2])

        # Execute DEJMPS Protocol
        result = three_to_one_protocol_alice(qubits[0],qubits[1],qubits[2],alice,socket)
        print(result, "ALICE")

        fid0 = None
        fid1 = None
        fid2_original = None
        fid2_new = None

        if result:
            a2_new_state = get_qubit_state(qubits[2])

            # Receive Bob's dms
            b0_state = numpy.array(eval(socket.recv()))
            b1_state = numpy.array(eval(socket.recv()))
            b2_original_state = numpy.array(eval(socket.recv()))
            b2_new_state = numpy.array(eval(socket.recv()))

            # Convert saved states of Alice back to simulated qubit    
            a0_theta, a0_phi, _= bloch_sphere_rep(a0_state)
            a1_theta, a1_phi, _ = bloch_sphere_rep(a1_state)
            a2_original_theta, a2_original_phi, _= bloch_sphere_rep(a2_original_state)
            a2_new_theta, a2_new_phi, _ = bloch_sphere_rep(a2_new_state)

            a0_original_qubit = qubit_from(a0_phi,a0_theta)
            a1_qubit = qubit_from(a1_phi,a1_theta)
            a2_original_qubit = qubit_from(a2_original_phi,a2_original_theta)
            a2_new_qubit = qubit_from(a2_new_phi,a2_new_theta)

            # Calculate fidelity
            fid0 = get_fidelity(a0_original_qubit,b0_state)
            fid1 = get_fidelity(a1_qubit,b1_state)
            fid2_original = get_fidelity(a2_original_qubit,b2_original_state)
            fid2_new = get_fidelity(a2_new_qubit,b2_new_state)
            print(fid0, fid1, fid2_original, fid2_new)

        return {
            "result": result,
            "fidelity0": fid0,
            "fidelity1": fid1,
            "fidelity2": fid2_original,
            "new fidelity2": fid2_new
        }
if __name__ == "__main__":
    main()
