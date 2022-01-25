from epl import epl_protocol_alice
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

    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        
        # Create EPR Pair
        qubits = epr_socket.create(number=2)
        alice.flush()

        # Save original qubit states
        aliceOriginal0 = get_qubit_state(qubits[0])
        aliceOriginal1 = get_qubit_state(qubits[1])
        
        # Execute EPL Protocol
        result = epl_protocol_alice(qubits[0],qubits[1],alice,socket)
        print(result, "ALICE")

        fidelity0 = None
        fidelity1 = None
        newfidelity0 = None

        if result:
            # Receive Bob's dms
            bobOriginal0 = numpy.array(eval(socket.recv()))
            bobOriginal1 = numpy.array(eval(socket.recv()))
            bobNew0 = numpy.array(eval(socket.recv()))

            # Process Bob's dms
            theta0, phi0, r0 = bloch_sphere_rep(bobOriginal0)
            theta1, phi1, r1 = bloch_sphere_rep(bobOriginal1)
            thetaNew0, phiNew0, rNew0 = bloch_sphere_rep(bobNew0)
            b0 = qubit_from(phi0,theta0)
            b1 = qubit_from(phi1,theta1)
            bNew0 = qubit_from(phiNew0,thetaNew0)

            # Steps to calculate fidelity
            fidelity0 = get_fidelity(b0,aliceOriginal0)
            fidelity1 = get_fidelity(b1,aliceOriginal1)
            newfidelity0 = get_fidelity(bNew0,get_qubit_state(qubits[0]))
            print(fidelity0,fidelity1,newfidelity0)

        return {
            "result": result,
            "fidelity0": fidelity0,
            "fidelity1": fidelity1,
            "new fidelity0": newfidelity0
        }

if __name__ == "__main__":
    main()
