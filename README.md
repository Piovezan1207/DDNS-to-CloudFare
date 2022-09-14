<H1>Atualizdor de IP para DNS Dinamico usando a cloudfare.</H1>

Esta aplicação tem como objetivo verificar o IP externo atual do roteador e caso esteja diferente com o iP cadastrado no DNS na cloudfare, o mesmo será atualizado automaticamente.


<h2>Configuração da .env</h2>

<br>NAME_DNS= "\<URL cadastrada na cloudfare\>"
<br>X_AUTH_EMAIL="\<Email da conta cloudfare\>"
<br>X_AUTH_KEY="\<Global API Token cloudfare\>"
<br>ZONE_ID="\<ZONE_ID cloudfare\>"
<br>ACCOUNT_ID="\<ACCOUNT_ID cloudfare\>"
<br>TYPE="\<Tipo de DNS A - AAAA ...\>"
<br>TTL="\<Time to live \>"
<br>PROXIED=\<Será utilizado proxy? 0 ou 1, apenas booleano\>
<br><br>
Obs:* Lembre de criar a .env antes de buildar o caontainer.

<br><br>
<h2>Comandos Docker</h2>
Build docker iamge : docker build --tag dynamic-dns-cf .<br>
Run docker image : docker run -d --restart unless-stopped --name ddns-cf dynamic-dns-cf<br>
