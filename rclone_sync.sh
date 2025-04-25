#!/bin/sh

# use backup_server.sh file to create backup tar
# put them in a directory and use this to sync to a google drive or similar

# note only content inside directory will get synched
backup_directory="/mnt/backups/compressed_backup_files"

# the unencrypted remote (used to accumulate total storage size)
unencrypt_remote="gdrive"
# the encrypted drive (what we actually sync to with encryption)
encrypt_remote="gdriveEncrypt"
# the storage path on the remote i.e. the folder inside the remote root /homeserver
storage_path="backups"
# the sub directory to sync to inside the storage_path
directory_to_sync_to_on_remote="compressed"

echo "Starting sync of $backup_directory to remote $encrypt_remote:$storage_path/$directory_to_sync_to_on_remote..."

start=$(date +%s.%N)
rclone sync "$backup_directory" $encrypt_remote:$storage_path/$directory_to_sync_to_on_remote
end=$(date +%s.%N)

# note: we could also use 'time' here but this is nicer
runtime=$( echo "$end - $start" | bc -l )
echo "Sync time: ${runtime} seconds"

err=$?

if [ $err -eq 0 ]; then
        echo "Sync successful"
else
        echo "ERROR WHILE SYNCHING BACHUPS"
fi

echo ""
echo ""

echo "Used storage:"
rclone size $unencrypt_remote:

echo ""
echo "'homeserver' directory files:"
rclone ls $encrypt_remote:$storage_path

echo ""
echo "Remote Infor"
rclone about $encrypt_remote:

