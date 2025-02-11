# Letrehoz egy tanusitvanyt a BNR adataival (2)
`openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out bnr_fake.key`  
`openssl req -x509 -new -key bnr_fake.key -days 69 -out bnr_fake.crt -subj "/CN=*.bnr.ro/O=Banca Nationala a Romaniei/C=RO/ST=Bucuresti/L=Bucuresti"`  
`openssl pkcs12 -export -in bnr_fake.crt -inkey bnr_fake.key -out bnr_fake.p12`  
`keytool -importkeystore -srckeystore bnr_fake.p12 -srcstoretype PKCS12 -destkeystore bnr_fake.jks -deststoretype JKS -storepass admin1`  

# Root CA letrehozasa (3)
`openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out RootCA.key`  
`openssl req -x509 -new -key RootCA.key -days 69 -out RootCA.crt -subj "/CN=bnim2219-RootCA/O=BBTE/C=RO/ST=Kolozs/L=Kolozsvár"`  

# ClientCA letrehozasa (3)
`openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ClientCA.key`  
`openssl req -new -key ClientCA.key -out ClientCA.csr -subj "/CN=bnim2219-ClientCA/O=BBTE/C=RO/ST=Kolozs/L=Kolozsvár"`  
`openssl x509 -req -in ClientCA.csr -CA RootCA.crt -CAkey RootCA.key -CAcreateserial -out ClientCA.crt -days 69`  

# ServerCA letrehozasa (3)
`openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ServerCA.key`   
`openssl req -new -key ServerCA.key -out ServerCA.csr -subj "/CN=bnim2219-ServerCA/O=BBTE/C=RO/ST=Kolozs/L=Kolozsvár"`  
`openssl x509 -req -in ServerCA.csr -CA RootCA.crt -CAkey RootCA.key -CAcreateserial -out ServerCA.crt -days 69`  

# kliens tanusitvany (4)
`openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out client.key`  
`openssl req -new -key client.key -out client.csr -subj "/C=RO/ST=Kolozs/L=Kolozsvár/O=BBTE/CN=bnim2219-client"`  
`openssl x509 -req -in client.csr -CA ClientCA.crt -CAkey ClientCA.key -CAcreateserial -out client.crt -days 69`  

# server tanusitvany (5)
`openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out server.key`  
`openssl req -new -key server.key -out server.csr -subj "/C=RO/ST=Kolozs/L=Kolozsvár/O=BBTE/CN=localhost"`  
`openssl x509 -req -in server.csr -CA ServerCA.crt -CAkey ServerCA.key -CAcreateserial -out server.crt -days 69`  

# server keystore (6)
`openssl pkcs12 -export -in server.crt -inkey server.key -name server -out server.p12 -passout pass:admin1`  
`keytool -importkeystore -srckeystore server.p12 -srcstoretype PKCS12 -srcstorepass admin1 -destkeystore server_keystore.jks -deststorepass admin1 -alias server`  

# kliens keystore (6)
`openssl pkcs12 -export -in client.crt -inkey client.key -name client -out client.p12 -passout pass:admin1`  
`keytool -importkeystore -srckeystore client.p12 -srcstoretype PKCS12 -srcstorepass admin1 -destkeystore client_keystore.jks -deststorepass admin1 -alias client`  


# server truststore (6)
`keytool -import -alias client -file client.crt -keystore server_truststore.jks -storepass admin1 -noprompt`  

# kliens truststore (6)
`keytool -import -alias server -file server.crt -keystore client_truststore.jks -storepass admin1 -noprompt`  
