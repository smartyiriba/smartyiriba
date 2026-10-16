#!/usr/bin/env python3
"""Publie le projet biz.smartyiriba.org sur le dépôt Git configuré.

Usage :
    python github-biz.py                 # prépare, commit et pousse
    python github-biz.py --dry-run       # vérifie sans modifier Git ni pousser
    python github-biz.py -m "Mon message" # utilise un message personnalisé

Le script utilise l'authentification déjà configurée pour Git (credential
helper, SSH ou GitHub CLI). Aucun jeton n'est stocké dans ce fichier.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


class GitError(RuntimeError):
    """Erreur lisible lors d'une commande Git."""


def run_git(*args: str, cwd: Path, dry_run: bool = False) -> str:
    command = ["git", *args]
    print("$", " ".join(command))
    if dry_run:
        return ""
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        raise GitError(f"{' '.join(command)}\n{details}")
    return result.stdout.strip()


def git_root() -> Path:
    raw = run_git("rev-parse", "--show-toplevel", cwd=PROJECT_DIR)
    root = Path(raw).resolve()
    if not (root / ".git").exists():
        raise GitError(f"Dépôt Git introuvable dans {root}")
    return root


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-m",
        "--message",
        default="Update Smart YIRIBA business website",
        help="message du commit (défaut : %(default)s)",
    )
    parser.add_argument(
        "--remote",
        default=os.getenv("GITHUB_REMOTE", "origin"),
        help="nom du remote Git (défaut : origin ou GITHUB_REMOTE)",
    )
    parser.add_argument(
        "--branch",
        default=os.getenv("GITHUB_BRANCH"),
        help="branche cible (défaut : branche courante ou GITHUB_BRANCH)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="affiche les contrôles sans staged files, commit ni push",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = git_root()
        project_rel = PROJECT_DIR.relative_to(root)
        if str(project_rel) in ("", "."):
            raise GitError("Le script doit se trouver dans un sous-dossier du dépôt")

        branch = args.branch or run_git("branch", "--show-current", cwd=root)
        if not branch:
            raise GitError("Impossible de déterminer la branche courante")

        remotes = run_git("remote", cwd=root).splitlines()
        if args.remote not in remotes:
            raise GitError(
                f"Remote '{args.remote}' introuvable. Remotes disponibles : "
                + (", ".join(remotes) or "aucun")
            )
        remote_url = run_git("remote", "get-url", args.remote, cwd=root)
        print(f"Dépôt : {root}")
        print(f"Projet ciblé : {project_rel}")
        print(f"Remote : {args.remote} ({remote_url})")
        print(f"Branche : {branch}")

        # Le .gitignore du projet protège déjà .env, .venv, SQLite, media,
        # staticfiles et tmp. Le chemin explicite empêche de publier le reste
        # du dépôt (par exemple Archive.zip à la racine).
        target = str(project_rel)
        run_git("add", "--all", "--", target, cwd=root, dry_run=args.dry_run)

        staged = run_git("diff", "--cached", "--name-only", cwd=root, dry_run=args.dry_run)
        if not args.dry_run and not staged:
            print("Aucun changement à publier.")
            return 0
        if args.dry_run:
            print("Mode vérification : aucun fichier n'a été modifié.")
            return 0

        run_git("commit", "-m", args.message, cwd=root)
        run_git("push", "-u", args.remote, branch, cwd=root)
        print("Publication GitHub terminée.")
        return 0
    except GitError as exc:
        print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError:
        print("Erreur : Git n'est pas installé ou absent du PATH.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
