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
        aliceOriginal0 = get_qubit_state(qubits[0])
        aliceOriginal1 = get_qubit_state(qubits[1])
        aliceOriginal2 = get_qubit_state(qubits[2])

        # Execute DEJMPS Protocol
        result = three_to_one_protocol_alice(qubits[0],qubits[1],qubits[2],alice,socket)
        print(result, "ALICE")

        fidelity0 = None
        fidelity1 = None
        fidelity2 = None
        newfidelity0 = None

        if result:
            # Receive Bob's dms
            bobOriginal0 = numpy.array(eval(socket.recv()))
            bobOriginal1 = numpy.array(eval(socket.recv()))
            bobOriginal2 = numpy.array(eval(socket.recv()))
            bobNew2 = numpy.array(eval(socket.recv()))

            # Process Bob's dms
            theta0, phi0, r0 = bloch_sphere_rep(bobOriginal0)
            theta1, phi1, r1 = bloch_sphere_rep(bobOriginal1)
            theta2, phi2, r2 = bloch_sphere_rep(bobOriginal2)
            thetaNew2, phiNew2, rNew2 = bloch_sphere_rep(bobNew2)
            b0 = qubit_from(phi0,theta0)
            b1 = qubit_from(phi1,theta1)
            b2 = qubit_from(phi2,theta2)
            bNew2 = qubit_from(phiNew2,thetaNew2)

            # Steps to calculate fidelity
            fidelity0 = get_fidelity(b0,aliceOriginal0)
            fidelity1 = get_fidelity(b1,aliceOriginal1)
            fidelity2 = get_fidelity(b2,aliceOriginal2)
            newfidelity0 = get_fidelity(bNew2,get_qubit_state(qubits[2]))
            print(fidelity0,fidelity1,fidelity2,newfidelity0)

        return {
            "result": result,
            "fidelity0": fidelity0,
            "fidelity1": fidelity1,
            "fidelity2": fidelity2,
            "new fidelity0": newfidelity0
        }
if __name__ == "__main__":
    main()
