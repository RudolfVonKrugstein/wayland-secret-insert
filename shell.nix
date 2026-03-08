{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  packages = with pkgs; [
    python3
    python3Packages.pygobject3
    libsecret
    gobject-introspection
    pkg-config
    cairo
    wofi
    zenity
  ];
  shellHook = ''
    export UV_PYTHON=$(which python)
    export UV_SYSTEM_PYTHON=1
    export UV_VENV_CLEAR=1
  '';
}
