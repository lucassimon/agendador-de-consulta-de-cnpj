$ psql -h localhost -U postgres
postgres=# create user agendadorcnpj with encrypted password 'teste123';
postgres=# create database agendadorcnpj;
postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO agendadorcnpj;


CREATE DATABASE agendadorcnpj;
CREATE USER agendador WITH ENCRYPTED PASSWORD 'teste';
GRANT ALL PRIVILEGES ON DATABASE agendadorcnpj TO agendador;
\c agendadorcnpj postgres
# You are now connected to database "agendadorcnpj" as user "postgres".
GRANT ALL ON SCHEMA public TO agendador;


---

- [X] backend (API REST)
- [X] banco de dados PostgreSQL
- [ ] sistema de enfileiramento (RABBITMQ/SQS)
- [ ] Docker
- [ ] Testes
- [ ] Chamadas assincronas
- [X] autenticação e autorização
- [ ] replicação de dados,
- [ ] detecção e recuperação de falhas
- [ ] além de monitoramento contínuo do sistema
- [ ] Um formulário de agendamento é fornecido
- [ ] Os agendamentos existentes são exibidos em uma lista ou calendário, permitindo a edição ou exclusão das tarefas agendadas.

---

- [ ] Um algoritmo é utilizado para selecionar a próxima tarefa da fila com base em critérios como ordem de chegada ou prioridade
- [ ] E-mails são enviados no início e no final de cada tarefa
-

---

- [ ] agendador interno envia um resumo diário das tarefas realizadas às 7 horas da noite

---

- [ ] A documentação do projeto é essencial para facilitar a compreensão e manutenção do código. É recomendado incluir um guia de instalação, guia de configuração, guia de uso, estrutura do código, explicação das principais funcionalidades, lista de dependências e
bibliotecas utilizadas, além de boas práticas de desenvolvimento, como padrões de codificação.

---

- [ ] O sistema deve ser executável e testável em um ambiente local.


---

https://www.youtube.com/watch?v=y8zY14HHiPI&list=PLP5_A7hnY1Tggph0F0cRqf5iyyZuIBXYC
https://www.youtube.com/watch?v=a3e1bRnq0rY
https://www.youtube.com/watch?v=ECMbSLxLRbc
https://github.com/Xewdy444/Playwright-reCAPTCHA
https://github.com/xrip/playwright-hcaptcha-solver
https://youtu.be/MKiCVRHeSHg
https://github.com/topics/hcaptcha-solver
https://github.com/Wikidepia/hektCaptcha-extension
https://www.zenrows.com/blog/playwright-captcha
https://stackoverflow.com/questions/72247022/is-there-any-way-to-bypass-hcaptcha-by-using-selenium-python


https://github.com/JustTalDevelops/go-hcaptcha


---

https://youtu.be/bfelC61XKO4
