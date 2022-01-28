from bbpssw import bbpssw_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import get_fidelity, to_dm, qubit_from
from netqasm.util.states import bloch_sphere_rep
import numpy

def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice","bob")
    
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob", min_fidelity= 0)

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket]
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's BBPSSW method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        
        # Create EPR Pair
        qubits = epr_socket.create(number=2)
        alice.flush()
        
        # Save state of original qubits
        a0_original_state = get_qubit_state(qubits[0])
        a1_state = get_qubit_state(qubits[1])

        # Execute BBPSSW Protocol
        result = bbpssw_protocol_alice(qubits[0],qubits[1],alice,socket)
        print(result, "ALICE")

        fid0_original = None
        fid1 = None
        fid0_new = None

        if result:
            a0_new_state = get_qubit_state(qubits[0])

            # Receive Bob's dms
            b0_original_state = numpy.array(eval(socket.recv()))
            b1_state = numpy.array(eval(socket.recv()))
            b0_new_state = numpy.array(eval(socket.recv()))

            # Convert saved states of Alice back to simulated qubit    
            a0_original_theta, a0_original_phi, _= bloch_sphere_rep(a0_original_state)
            a1_theta, a1_phi, _ = bloch_sphere_rep(a1_state)
            a0_new_theta, a0_new_phi, _= bloch_sphere_rep(a0_new_state)

            a0_original_qubit = qubit_from(a0_original_phi,a0_original_theta)
            a1_qubit = qubit_from(a1_phi,a1_theta)
            a0_new_qubit = qubit_from(a0_new_phi,a0_new_theta)

            # Calculate fidelity
            fid0_original = get_fidelity(a0_original_qubit,b0_original_state)
            fid1 = get_fidelity(a1_qubit,b1_state)
            fid0_new = get_fidelity(a0_new_qubit,b0_new_state)
            print(fid0_original, fid1, fid0_new)

        return {
            "result": result,
            "fidelity0": fid0_original,
            "fidelity1": fid1,
            "new fidelity0": fid0_new
        }

if __name__ == "__main__":
    main()
