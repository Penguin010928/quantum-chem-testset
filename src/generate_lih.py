from openfermion import MolecularData
from openfermionpyscf import run_pyscf
from openfermion.transforms import jordan_wigner
from openfermion.utils import count_qubits
import json
import os

# ========== 参数配置 ==========
GEOMETRY = [
    ('Li', [0.0, 0.0, 0.0]),
    ('H',  [0.0, 0.0, 1.6])
]
BASIS = 'sto-3g'
OUTPUT_DIR = os.path.join('data', 'molecules')
OUTPUT_FILE = 'LiH_sto3g.json'
# =============================

def generate_lih_data():
    # 确保输出目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 初始化分子模型
    molecule = MolecularData(
        geometry=GEOMETRY,
        basis=BASIS,
        multiplicity=1,
        charge=0,
        description="LiH_sto3g"
    )
    
    # 量子化学计算（可能需要更长时间）
    print("🔄 开始LiH的量子化学计算（约需3-5分钟）...")
    molecule = run_pyscf(
        molecule,
        run_scf=True,
        run_ccsd=True,
        run_fci=True,
    )
    
    # 哈密顿量转换
    fermionic_ham = molecule.get_molecular_hamiltonian()
    qubit_ham_jw = jordan_wigner(fermionic_ham)
    
    # 构建输出数据
    output = {
        "metadata": {
            "basis": BASIS,
            "n_qubits": count_qubits(qubit_ham_jw),
            "bond_length": 1.6
        },
        "energies": {
            "hf": molecule.hf_energy,
            "ccsd": molecule.ccsd_energy,
            "fci": molecule.fci_energy
        },
        "hamiltonian": {
            "fermionic_terms": repr(fermionic_ham),
            "qubit_terms_jw": str(qubit_ham_jw)
        }
    }
    
    # 保存文件
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"✅ LiH数据已保存至 {output_path}")
    print(f"   量子比特数: {output['metadata']['n_qubits']}")

if __name__ == "__main__":
    generate_lih_data()