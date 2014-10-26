cat /proc/mounts |  awk '{    if ( $1 ~ /\/dev/ ) 
   {
      num_elem = split($2,str_array,"/")
      if (str_array[num_elem] == "")
      {
         str_array[num_elem] = "/";
      }
      printf "%5.5s:  ${fs_free %s} / ${fs_size %s}\n${fs_bar 6 %s}\n", str_array[num_elem], $2, $2, $2
   }
}'
