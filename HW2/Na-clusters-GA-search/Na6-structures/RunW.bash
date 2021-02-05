#!/bin/bash
for i in {1..15..1}
  do
#      echo '#!/bin/bash'$'\n'"$(cat W$i.bash)" > W$i.bash
#      chmod +x W$i.bash	
       sbatch ./W$i.bash  
 done
