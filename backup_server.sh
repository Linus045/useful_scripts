#!/bin/sh

LOGFILE=/mnt/admin/rsync.log
ERRORLOGFILE=/mnt/admin/rsync_error.log
OUTPUTDIR=/mnt/admin/raw_backup
TARSOUTPUTDIR=/mnt/admin/compressed_backup_files

mkdir -p $TARSOUTPUTDIR

# clear file
truncate -s 0 $ERRORLOGFILE

# write header
echo "=============================================================================" > $LOGFILE
echo "Backup from: " >> $LOGFILE
date >> $LOGFILE
echo "=============================================================================" >> $LOGFILE

dirs_to_backup="/home /etc /var/www /var/spool/cron/crontabs /var/backups /root"

# this container contains large files that i don't want to backup
dir_to_exclude="/home/admin/IGNORE_IN_BACKUP"

rsync --info=name0 \
	--verbose \
	--human-readable \
	--update \
	--delete \
	--archive \
	--keep-dirlinks \
	--executability \
	--xattrs \
	--partial \
	--acls \
	--hard-links \
	--relative \
	--exclude $dir_to_exclude \
	$dirs_to_backup \
	$OUTPUTDIR/ 2>> $ERRORLOGFILE | tee $LOGFILE


echo "============================================================================="
echo "ERRORS: "
cat $ERRORLOGFILE
echo "============================================================================="


MAX_BACKUPS_TO_KEEP=8

current_backup_count=$(ls -1 --sort version $TARSOUTPUTDIR | wc -l)
echo "Backup count currently: $current_backup_count"


counter=0

for line in $(find $TARSOUTPUTDIR -maxdepth 1 -iname "backup_*" | sort -rV); do 
    counter=$((counter + 1));
    echo "$counter backup: $line";
    if [ $counter -gt $((MAX_BACKUPS_TO_KEEP-1)) ]; then
	echo "Deleting backupfile: $line";
	rm $line
     else
	echo "Keeping backupfile: $line";
    fi
done

curDate=$(date '+%Y_%m_%d_%H_%M')

newBackupFilename="$TARSOUTPUTDIR/backup_$curDate.tar.gz"
tar -czf $newBackupFilename --exclude $dir_to_exclude -C / $dirs_to_backup

echo "============================================================================="
echo "Created backup file: $newBackupFilename"
echo "Backups:"
ls -sh1 --sort version $TARSOUTPUTDIR 
echo "============================================================================="
