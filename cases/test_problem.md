# cases/test_problem.md
## Enunciado

Implemente um serviço de deduplicação de eventos com expiração (TTL):

EventDeduper.seen(event_id: str, ttl_seconds: float) -> bool retorna True se o evento já foi visto dentro da janela de TTL, False caso contrário (e registra o evento).
Eventos expirados (fora do TTL) devem ser tratados como não vistos.
event_id vazio ou None deve levantar ValueError.
Assuma que múltiplas threads podem chamar seen() concorrentemente para o mesmo event_id.

Áreas de competência cobertas: concorrência, expiração/TTL, validação de entrada de dados.