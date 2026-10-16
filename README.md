# TimeQuant Docker Engines

Bienvenue dans le dépôt officiel de conteneurisation des moteurs de calcul pour la plateforme **TimeQuant**. Ce projet regroupe les environnements isolés, sécurisés et optimisés pour les **31 moteurs de calcul scientifique** (DFT, transport quantique, IA moléculaire, modèles analytiques, phonons) utilisés par TimeQuant.

---

## Contexte et Objectifs

La plateforme TimeQuant orchestre un écosystème hétérogène de codes de physique et chimie computationnelle. Afin d'éviter tout conflit de bibliothèques (Fortran, OpenMPI, ScaLAPACK, versions de GCC/C++, PyTorch, TensorFlow, Cython et NumPy), chaque moteur est strictement isolé dans sa propre image Docker.

### Garanties d'intégrité de chaque conteneur :
- **Authenticité 100 % (Zéro Mock, Zéro Stub)** : Aucun package factice ni contournement (`|| true`) ; chaque image exécute les vrais binaires et importe les véritables bibliothèques scientifiques.
- **Sécurité & Isolation non-root** : Chaque conteneur s'exécute avec l'utilisateur sécurisé `timequant:timequant` (`UID 1000:GID 1000`) travaillant dans `/workspace`.
- **Wrapper d'entrée unifié (`entrypoint-wrapper.sh`)** : Intercepte les flux, streame en direct `stdout`/`stderr`, enregistre une copie locale de `error.log` dans le dossier de travail monté et propage fidèlement le code de sortie réel de l'exécutable.
- **Optimisation de l'empreinte disque** : Utilisation d'images de base Debian Slim / Micromamba et de roues optimisées CPU pour permettre la cohabitation des 31 moteurs sur n'importe quel environnement de calcul ou CI/CD sans saturation d'espace.

---

##  Structure du Projet

```text
.
├── docker-engines/
│   ├── Makefile                     # Commandes d'aide (build-all, test-all, push-all)
│   ├── build_all.sh                 # Compilation unifiée ou ciblée des images
│   ├── test_all.sh                  # Suite de validation (smoke tests) des conteneurs
│   ├── REGISTRY.md                  # Registre des 31 moteurs, tags, tailles et statut de validation
│   ├── common/                      # Scripts partagés (entrypoint-wrapper.sh, test_runner.py)
│   ├── docs/                        # Documentation architecturale
│   └── engines/                     # Dossiers individuels des 31 moteurs
│       ├── qe/                      # (Quantum ESPRESSO)
│       ├── siesta/                  # (SIESTA DFT)
│       ├── cp2k/                    # (CP2K)
│       ├── pyscf/                   # (PySCF)
│       ├── mace/                    # (MACE MLIP)
│       └── ...
├── scaffold_engines.py              # Script générateur de configuration à la racine
└── scripts/
    └── scaffold_engines.py          # Script de scaffolding des moteurs
```

---

##  Registre des 31 Moteurs Validés

Tous les 31 moteurs sont construits et validés (tests d'intégrité au vert) :

| # | Moteur | Groupe | Tag Docker | Empreinte | Binaire / Bibliothèque validée |
|---|---|---|---|---|---|
| 1 | **qe** | 1 | `timequant/engine-qe:latest` | 718 MB | Quantum ESPRESSO (`pw.x`, `ph.x`, `pp.x`) |
| 2 | **siesta** | 1 | `timequant/engine-siesta:latest` | 651 MB | SIESTA DFT (`siesta`) |
| 3 | **cp2k** | 1 | `timequant/engine-cp2k:latest` | 478 MB | CP2K v9.1 MPI/OpenMP (`cp2k`) |
| 4 | **dftb** | 1 | `timequant/engine-dftb:latest` | 463 MB | DFTB+ (`dftb+`) |
| 5 | **openmx** | 1 | `timequant/engine-openmx:latest` | 674 MB | OpenMX DFT (`openmx`) |
| 6 | **vasp** | 1 | `timequant/engine-vasp:latest` | 220 MB | VASP (Wrapper BYOB - Bring Your Own Binary) |
| 7 | **yambo** | 1 | `timequant/engine-yambo:latest` | 1.01 GB | Yambo MBPT (`yambo`) |
| 8 | **wannier90** | 1 | `timequant/engine-wannier90:latest` | 240 MB | Wannier90 v3.x (`wannier90.x`) |
| 9 | **models** | 2 | `timequant/engine-models:latest` | 484 MB | Modèles analytiques (NumPy, SciPy) |
| 10 | **ase_tools** | 2 | `timequant/engine-ase_tools:latest` | 1.08 GB | ASE v3.29.0 & PyMatGen |
| 11 | **qeh** | 2 | `timequant/engine-qeh:latest` | 664 MB | Quantum Electrostatic Heterostructure (QEH v23.6.0) |
| 12 | **hetdb** | 2 | `timequant/engine-hetdb:latest` | 1.61 GB | HetBuilder v0.6.75 (extensions C++ compilées) |
| 13 | **sisl** | 2 | `timequant/engine-sisl:latest` | 708 MB | sisl v0.16.4 avec NetCDF4 et xarray |
| 14 | **phonopy** | 2 | `timequant/engine-phonopy:latest` | 1.14 GB | Phonopy v4.8.3, spglib, seekpath |
| 15 | **atomistics** | 2 | `timequant/engine-atomistics:latest` | 672 MB | atomistics v0.3.10 |
| 16 | **boltztrap** | 2 | `timequant/engine-boltztrap:latest` | 1.37 GB | BoltzTraP2 avec extension C++ Spglib |
| 17 | **amset** | 2 | `timequant/engine-amset:latest` | 2.04 GB | AMSET v0.5.1 avec BoltzTraP2 |
| 18 | **wannier_berri** | 2 | `timequant/engine-wannier_berri:latest` | 1.29 GB | WannierBerri v26.10 |
| 19 | **qutip** | 2 | `timequant/engine-qutip:latest` | 1.14 GB | QuTiP v5.3.1 (Quantum Toolbox in Python) |
| 20 | **pyscf** | 2 | `timequant/engine-pyscf:latest` | 1.36 GB | PySCF v2.14.0, geometric, pyberny |
| 21 | **gpaw** | 2 | `timequant/engine-gpaw:latest` | 1.44 GB | GPAW v26.7.0 (compilé C++ avec ASE et OpenBLAS) |
| 22 | **kwant** | 2 | `timequant/engine-kwant:latest` | 1.67 GB | Kwant v1.5.0 (transport quantique) |
| 23 | **tkwant** | 2 | `timequant/engine-tkwant:latest` | 1.78 GB | TKwant v1.1.0 (transport dépendant du temps) |
| 24 | **nanoworks** | 3 | `timequant/engine-nanoworks:latest` | 1.61 GB | Nanoworks v26.8.0 avec ASE et GPAW |
| 25 | **electronex** | 3 | `timequant/engine-electronex:latest` | 608 MB | ELEQTRONeX / electronex v0.1.0 |
| 26 | **pinn** | 3 | `timequant/engine-pinn:latest` | 1.77 GB | DeepXDE v1.15.0 avec backend PyTorch |
| 27 | **deeptb** | 3 | `timequant/engine-deeptb:latest` | 1.96 GB | DeePTB (dptb v2.2.1), PyG torch-scatter |
| 28 | **rhodent** | 3 | `timequant/engine-rhodent:latest` | 2.36 GB | Rhodent v1.1, e3nn, PyG torch-scatter |
| 29 | **deepgreen** | 3 | `timequant/engine-deepgreen:latest` | 4.38 GB | GreenLearning, TensorFlow, PyTorch Geometric |
| 30 | **mace** | 3 | `timequant/engine-mace:latest` | 1.83 GB | MACE v0.3.16 (mace-torch, ase, torch-geometric) |
| 31 | **kim** | 4 | `timequant/engine-kim:latest` | 714 MB | OpenKIM API (`kim-api-collections-management`) |

Consultez [REGISTRY.md](docker-engines/REGISTRY.md) pour les détails complets.

---

##  Compilation et Tests

Tous les scripts de compilation et de test supportent à la fois l'ensemble des moteurs ou un sous-ensemble ciblé.

### 1. Construire les images Docker :

```bash
cd docker-engines

# Construire tous les 31 moteurs
./build_all.sh

# Ou construire un ou plusieurs moteurs spécifiques :
./build_all.sh qe
./build_all.sh qe pyscf mace
```

### 2. Valider les conteneurs (Smoke Tests) :

Chaque conteneur exécute son script `test.sh` dédié sous l'UID 1000 :

```bash
cd docker-engines

# Tester tous les 31 moteurs
./test_all.sh

# Ou tester un moteur spécifique :
./test_all.sh qe
./test_all.sh mace
```

---

##  Utilisation Standardisée d'un Moteur (I/O)

Tous les conteneurs partagent une convention d'entrée/sortie uniforme pour une intégration transparente avec l'orchestrateur TimeQuant.

### Conventions :
1. **Montage du workspace** : Le répertoire de calcul sur l'hôte doit être monté sur `/workspace` dans le conteneur (`-v /path/to/task:/workspace -w /workspace`).
2. **Utilisateur non-root** : L'exécution s'effectue sous `--user 1000:1000`.
3. **Capture des erreurs** : Le wrapper génère automatiquement `/workspace/error.log` en cas d'erreur tout en affichant la sortie standard.

### Exemples d'Exécution :

**Moteur DFT Fortran/MPI (ex: Quantum ESPRESSO) :**
```bash
docker run --rm \
  --user 1000:1000 \
  -v /chemin/vers/task:/workspace \
  -w /workspace \
  timequant/engine-qe:latest \
  -c "pw.x < scf.in > scf.out"
```

**Moteur Python Scientifique (ex: PySCF) :**
```bash
docker run --rm \
  --user 1000:1000 \
  -v /chemin/vers/task:/workspace \
  -w /workspace \
  timequant/engine-pyscf:latest \
  -c "python3 molecule_calc.py"
```

**Moteur IA Moléculaire (ex: MACE avec GPU optionnel) :**
```bash
docker run --rm \
  --gpus all \
  --user 1000:1000 \
  -v /chemin/vers/task:/workspace \
  -w /workspace \
  timequant/engine-mace:latest \
  -c "python3 evaluate_structure.py"
```

**Moteur Propriétaire VASP (Mode BYOB) :**
```bash
# Montez votre binaire sous licence vasp_std dans /usr/local/bin/vasp_std
docker run --rm \
  --user 1000:1000 \
  -v /chemin/vers/mon_vasp_std:/usr/local/bin/vasp_std:ro \
  -v /chemin/vers/calcul_vasp:/workspace \
  -w /workspace \
  timequant/engine-vasp:latest \
  -c "vasp_std"
```

---

##  Déploiement vers un Registre Docker

Pour déployer les images construites vers un registre distant (Docker Hub, GitHub Container Registry ou registre d'entreprise privé) :

### Option 1 : Docker Hub
```bash
# 1. Connexion au registre
docker login

# 2. Pousser une image ou l'ensemble
docker push timequant/engine-qe:latest
docker push timequant/engine-mace:latest
```

### Option 2 : GitHub Container Registry (GHCR)
```bash
# 1. Connexion avec un Personal Access Token (PAT)
echo $GHCR_PAT | docker login ghcr.io -u <VOTRE_USER_GITHUB> --password-stdin

# 2. Taguer et pousser
docker tag timequant/engine-qe:latest ghcr.io/<VOTRE_USER_GITHUB>/timequant-engine-qe:latest
docker push ghcr.io/<VOTRE_USER_GITHUB>/timequant-engine-qe:latest
```
