from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import register, available_backends, get_backend, execute

# Settings
LOCAL = False
USE_SIMULATOR = True
SHOTS_SIM = 100

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
			backend = "ibmqx5"

		else:
			backend = "ibmq_qasm_simulator"

	try:
		# Create a quantum register with 2 qbits
		q = QuantumRegister(4)

		# Create a classical register with 2 bits
		c = ClassicalRegister(4)

		# Create a quantum circuit
		qc = QuantumCircuit(q, c)


		# Add a H gate on qubit 0, putting this qubit in superposition
		qc.h(q[0])

		# Add a CX (CNOT) gate on control qubit 0 and target qubit 1 putting
		# putting qubits in bell state
		qc.cx(q[0], q[1])

		# Add a measure gate to see the state
		qc.measure(q, c)

		# See a list of available local simulators
		# print("Local Backends: ", available_backends({'local': True}))

		# Compile and execute
		job_sim = execute(qc, backend)
		sim_result = job_sim.result()

		# Display result
		print("Simulation: ", sim_result)
		print(sim_result.get_counts(qc))

	except Exception as e:
		print('There was an exception. {}'.format(e))