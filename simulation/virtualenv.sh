#!/bin/bash

function INIT()
{
    source "venv/bin/activate"
    NOW=$(date +"%d.%m.%Y %T")
    echo
    echo "> Ambiente virtual INICIADO! =)"
    echo "> data:" $NOW
    echo "> usuário:" $USER
    echo "> versão:" $(python3 --version)
    echo
    # FOR LOG
    echo "> Ambiente virtual INICIADO! =)" >> now.log
    echo "> data:" $NOW >> now.log
    echo "> usuário:" $USER >> now.log
    echo "> versão:" $(python3 --version) >> now.log
    echo >> now.log
}

function CLOSE()
{
    deactivate
    NOW=$(date +"%d.%m.%Y %T")
    echo
    echo "> Ambiente virtual ENCERRADO! =("
    echo "> data:" $NOW
    echo "> usuário:" $USER
    echo "> versão:" $(python3 --version)
    echo
    # FOR LOG
    echo "> Ambiente virtual ENCERRADO! =(" >> now.log
    echo "> data:" $NOW >> now.log
    echo "> usuário:" $USER >> now.log
    echo "> versão:" $(python3 --version) >> now.log
    echo >> now.log

}

if [ -z $1 ]
then
    echo "Verifique os parametros!"
    echo "$ source virtualenv init | close"
elif [ $1 == 'init' ]
then
    INIT;
elif [ $1 == 'close' ]
then
    CLOSE;
else
    echo "Comando inválido! Tente init ou close."
fi