from openfermion import MolecularData
from openfermionpyscf import run_pyscf
from openfermion.transforms import jordan_wigner
from openfermion.utils import count_qubits
import json
import os

# 配置参数
geometry = [('H', (0.0, 0.0, 0.0)), ('H', (0.0, 0.0, 0.74))]
basis = 'sto-3g'
output_dir = os.path.join('data', 'molecules')
os.makedirs(output_dir, exist_ok=True)

# 计算并保存数据
molecule = MolecularData(geometry, basis, multiplicity=1, charge=0)
molecule = run_pyscf(molecule, run_scf=True, run_ccsd=True, run_fci=True)
fermionic_ham = molecule.get_molecular_hamiltonian()
qubit_ham_jw = jordan_wigner(fermionic_ham)

output = {
    "metadata": {
        "basis": basis,
        "n_qubits": count_qubits(qubit_ham_jw)
    },
    "energies": {
        "hf": molecule.hf_energy,
        "fci": molecule.fci_energy
    },
    "hamiltonian": {
            "fermionic_terms": str(fermionic_ham),
            "qubit_terms_jw": str(qubit_ham_jw)
    }
}

with open(os.path.join(output_dir, 'H2_sto3g.json'), 'w') as f:
    json.dump(output, f, indent=2)

print(f"✅ 数据已保存到 {os.path.abspath(output_dir)}/H2_sto3g.json")