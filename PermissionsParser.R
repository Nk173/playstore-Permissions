## Parsing Scrapy output csv

# Identify unique row condition
Perm<-data.frame(name = permissions_app_playstore_paid$Name,LastUpdate = permissions_app_playstore_paid$LastUpdate ,Version = permissions_app_playstore_paid$Version, Permissions = permissions_app_playstore_paid$Permissions)

# getting each Permission from the Permissions column which have two delimiters \n and ,
# install.packages("splitstackshape")
library(splitstackshape)
Perm1<-cSplit(Perm, 'Permissions', sep="\n" , type.convert=FALSE)
Perm2<-cSplit(Perm1, 4:ncol(Perm1), sep="," , type.convert=FALSE)

## reshaping to get each permission as column
library(reshape2)
Perm3<- melt(Perm2, id.vars=c('name', 'Version', 'LastUpdate'),var='Permissions', na.rm=FALSE)
Perm5<- dcast(Perm3, name+Version+LastUpdate ~ value )
# u_perms<- unique(Perm5$value)

Permissions_final <-merge(permissions_app_playstore_paid, Perm5, by.x = c("Name","Version","LastUpdate"), by.y = c("name","Version","LastUpdate"))
write.csv(Permissions_final, file = "C:/Python27/test/playstore/playstore/Permissionspaid__final.csv")
