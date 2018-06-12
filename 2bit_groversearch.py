from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import register, available_backends, get_backend, execute

# import basic plot tools
from qiskit.tools.visualization import plot_histogram, circuit_drawer

# Settings
LOCAL = True
USE_SIMULATOR = True
MAX_CREDIT = 3
SHOTS = 1024
QUBITS = 5

# Load config
if __name__ == '__main__':
	if LOCAL:
		# Local backends available
		# 'local_statevector_simulator', 'local_clifford_simulator', 'local_qasm_simulator', 'local_unitary_simulator'
		backend = "local_qasm_simulator"

	else:
		try:
			import Qconfig
			qx_config = {
				"APIToken": Qconfig.APIToken,
				"url": Qconfig.config['url']
			}

		except Exception as e:
			print(e)
			qx_config = {
				"APIToken": "Insert Token Here",
				"url": "https://quantumexperience.ng.bluemix.net/api"
				}

		# Use simulator
		if not USE_SIMULATOR:
			if QUBITS == 5:
				backend = "ibmqx4"
			elif QUBITS == 16:
				backend = "ibmqx5"
			else:
				print("Only 5 Qubit and 16 Qubit quantum computer is available.")

		else:
			backend = "ibmqx_qasm_simulator"

	try:
		# bit size 
		N = 2

		# Create a quantum register with 2 qbits
		q = QuantumRegister(N)

		# Create a classical register with 2 bits
		c = ClassicalRegister(N)

		# Create a quantum circuit
		qc = QuantumCircuit(q, c)

		######################
		#    	ORACLE		 #
		######################

		# Apply H to all qubits to superpose
		for i in range(N):
			qc.h(q[i])

		# Apply S (Clifford phase gate) to all qubits
		for i in range(N):
			qc.s(q[i])

		# Apply CZ 
		qc.cz(q[0], q[1])

		# Reapply in reverse
		for i in range(N):
			qc.s(q[i])

		for i in range(N):
			qc.h(q[i])


		######################
		#    INV ABOUT MEAN	 #
		######################

		# Apply X to all bits
		for i in range(N):
			qc.x(q[i])

		# Apply CZ
		qc.cz(q[0], q[1])

		# Apply X to all bitss
		for i in range(N):
			qc.x(q[i])

		# Apply H to all bits				
		for i in range(N):
			qc.h(q[i])

		# Add a measure gate to see the state
		qc.measure(q, c)

		# See a list of available local simulators
		# print("Local Backends: ", available_backends({'local': True}))

		# Compile and execute
		if LOCAL:
			job_exp = execute(qc, backend)
		else:
			job_exp = execute(qc, backend, shots = SHOTS, max_credits = MAX_CREDIT)
			
		result = job_exp.result()

		# Display result
		print("Results: ", result)
		print(result.get_counts(qc))
		print(result.get_data())

		circuit_drawer(qc)

	except Exception as e:
		print('There was an exception. {}'.format(e))