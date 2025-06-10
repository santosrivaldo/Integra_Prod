#!/bin/bash

set -e

echo "Atualizando pacotes..."
sudo apt update -y
sudo apt upgrade -y

echo "Removendo versões antigas do Docker, se houver..."
sudo apt remove -y docker docker-engine docker.io containerd runc || true

echo "Instalando dependências..."
sudo apt install -y ca-certificates curl gnupg lsb-release apt-transport-https software-properties-common

echo "Adicionando chave GPG oficial do Docker..."
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo "Adicionando repositório oficial do Docker..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Atualizando índice de pacotes com Docker..."
sudo apt update -y

echo "Instalando Docker Engine, CLI e containerd..."
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "Adicionando usuário atual ao grupo docker..."
sudo usermod -aG docker $USER

echo "Docker instalado com sucesso!"
echo "Você precisará reiniciar a sessão ou rodar 'newgrp docker' para aplicar o grupo."

