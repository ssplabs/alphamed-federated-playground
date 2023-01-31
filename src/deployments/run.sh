#!/bin/bash
root_path="/data/www/federated-service/"
init_() {

  if [ ! -d "${root_path}/logs/" ]; then
    ln -s /logs "${root_path}/logs"
  else
    echo "${root_path}/logs 已存在"
  fi
  cd $root_path;
  /usr/local/bin/supervisord
  tail -f /var/log/supervisord/supervisord.log
}
start_() {
  supervisorctl start federated-service-web
  supervisorctl start federated-service-workers

}

stop_() {
  supervisorctl stop federated-service-web
  supervisorctl stop federated-service-workers


}

restart() {
  supervisorctl restart alphaMed-fed-service-web
  supervisorctl restart alphaMed-fed-service-workers

}

help_() {
  echo ''
  echo 'usage:'
  echo '      ./run.sh            init the program required'
  echo '      ./run.sh start      start the program'
  echo '      ./run.sh stop       stop the program'
  echo '      ./run.sh restart    restart the program'
  echo ''
}

main() {
  argu=$1

  if [ "$argu" = "" ]; then
    init_
  elif [ "$argu" = "start" ]; then
    start_
  elif [ "$argu" = "stop" ]; then
    stop_
  elif [ "$argu" = "restart" ]; then
    restart
  else
    help_
  fi
}

main $1
