
# Crea tutte le cartelle mancanti, inserite in conf/ftp.conf

for plant_dir in `cat conf/ftp.conf | grep 'dir:'|cut -d' ' -f6`;
do
  if [ -d $plant_dir ]
  then
    echo "$plant_dir exist"
  else
    echo "Create new dir $plant_dir"
    mkdir $plant_dir
    chown www-data:www-data $plant_dir
  fi
done

