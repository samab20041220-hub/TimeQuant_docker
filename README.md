# TimeQuant Docker Engines

Bienvenue dans le dépôt de conteneurisation des moteurs de calcul pour la plateforme **TimeQuant**. Ce projet regroupe les environnements isolés et optimisés pour les **31 moteurs de calcul scientifique** (DFT, transport quantique, IA moléculaire, modèles analytiques) utilisés par TimeQuant.

## 🚀 Contexte et Objectifs

La plateforme TimeQuant orchestre de nombreux moteurs hétérogènes. Afin d'éviter les conflits de bibliothèques (Fortran, MPI, BLAS, Python, CUDA), chaque moteur a été isolé dans sa propre image Docker.

Chaque image contient :
* Les binaires et bibliothèques natives requises.
* Les dépendances spécifiques (ex: OpenMPI, NetCDF, ScaLAPACK).
* Le paramétrage d'exécution optimisé pour l'isolation.

---

## 🏗️ Structure du Projet

```text
.
├── docker-engines/
│   ├── Makefile                     # Commandes d'aide
│   ├── build_all.sh                 # Script de compilation de toutes les images
│   ├── test_all.sh                  # Script d'exécution des tests unifiés
│   ├── REGISTRY.md                  # Registre de l'état et des tags des 31 moteurs
│   ├── common/                      # Scripts partagés (wrappers, runners)
│   ├── docs/                        # Documentation architecturale
│   └── engines/                     # Contient les 31 dossiers, un pour chaque moteur
│       ├── qe/                      # (Quantum ESPRESSO)
│       ├── siesta/
│       ├── pyscf/
│       └── ...
```

---

## ⚙️ Compilation et Tests Globaux

Pour construire l'ensemble des 31 images Docker (attention, cela peut prendre beaucoup de temps et d'espace disque) :

```bash
cd docker-engines
./build_all.sh
```

Pour lancer la suite de tests validant l'exécution de chaque moteur :

```bash
cd docker-engines
./test_all.sh
```

---

## 🔌 Utilisation Individuelle d'un Moteur (I/O Standardisé)

Tous les conteneurs partagent une interface unifiée afin d'être appelés de façon transparente par l'orchestrateur TimeQuant.

### Convention de Montage
- Le répertoire de travail généré sur l'hôte (ex: `/path/to/tasks/task_123`) doit être monté dans `/workspace` au sein du conteneur.
- Le conteneur s'exécute sans les privilèges administrateurs (`UID 1000:GID 1000`) pour éviter les problèmes de permissions sur les fichiers de résultats.

### Commande de Démarrage Individuel

Voici la commande standard pour démarrer **n'importe quel moteur** (remplacez `<engine_name>` par le nom du moteur, ex: `qe`, `pyscf`, `mace`) :

```bash
docker run --rm \
  --user 1000:1000 \
  -v /chemin/absolu/vers/votre/dossier_task:/workspace \
  -w /workspace \
  timequant/engine-<engine_name>:latest \
  <executable_ou_script_specifique> [arguments...]
```

**Exemple concret pour Quantum ESPRESSO (`qe`) :**
```bash
docker run --rm \
  --user 1000:1000 \
  -v /home/user/tasks/task_001:/workspace \
  -w /workspace \
  timequant/engine-qe:latest \
  -c "pw.x < input.pwi > output.pwo"
```

**Exemple concret pour un moteur GPU (`mace`) :**
*Note: Ajoutez l'argument `--gpus all` pour l'accélération matérielle.*
```bash
docker run --rm \
  --gpus all \
  --user 1000:1000 \
  -v /home/user/tasks/task_002:/workspace \
  -w /workspace \
  timequant/engine-mace:latest \
  -c "python3 run_mace.py"
```

---

## 🗂️ Groupes de Moteurs

Les 31 moteurs sont divisés en 4 groupes selon leur typologie technologique :

* **🟢 GROUPE 1 : Moteurs DFT Ab-Initio & Semi-Empiriques (Fortran/C/MPI)**
  * *Exemples :* Quantum ESPRESSO (`qe`), SIESTA (`siesta`), CP2K (`cp2k`), VASP (`vasp`), Yambo (`yambo`).
  * *Base :* `ubuntu:22.04` + OpenMPI.

* **🔵 GROUPE 2 : Moteurs Python Scientifiques, Chimie & Transport**
  * *Exemples :* GPAW (`gpaw`), PySCF (`pyscf`), Kwant (`kwant`), Phonopy (`phonopy`).
  * *Base :* `python:3.11-slim` + GCC/Pip.

* **🟣 GROUPE 3 : IA Moléculaire, Graph Neural Networks & MLIP (GPU/CUDA)**
  * *Exemples :* MACE (`mace`), DeePTB (`deeptb`), PINN (`pinn`).
  * *Base :* `pytorch/pytorch:2.2.0-cuda12.1-cudnn8-runtime`.

* **⚪ GROUPE 4 : Outils, Bases & Modèles Analytiques**
  * *Exemples :* OpenKIM (`kim`), HetDB (`hetdb`), Modèles analytiques (`models`).
  * *Base :* Légères (`python:3.12-slim` ou `ubuntu`).

Consultez `docker-engines/REGISTRY.md` pour l'état détaillé de chaque tag.
