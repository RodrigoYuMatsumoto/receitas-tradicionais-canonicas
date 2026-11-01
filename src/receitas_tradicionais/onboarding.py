"""Entrada culinária reconhecível, compartilhada pela conversa e pelo terminal."""

from __future__ import annotations

CHECKLIST = (
    {"id": "1", "group": "Leite e derivados", "examples": ["leite", "lactose", "queijo", "manteiga", "creme de leite", "iogurte"]},
    {"id": "2", "group": "Ovos", "examples": ["clara", "gema", "maionese", "massas e empanados com ovo"]},
    {"id": "3", "group": "Cereais e farinhas", "examples": ["trigo", "glúten", "centeio", "cevada", "aveia", "milho"]},
    {"id": "4", "group": "Soja, amendoim e sementes", "examples": ["soja", "tofu", "molho de soja", "amendoim", "gergelim", "mostarda"]},
    {"id": "5", "group": "Castanhas e semelhantes", "examples": ["castanha-de-caju", "castanha-do-pará", "nozes", "amêndoas", "avelãs", "pistache", "coco"]},
    {"id": "6", "group": "Peixes e frutos do mar", "examples": ["peixe", "camarão", "caranguejo", "lagosta", "lula", "polvo", "mariscos"]},
    {"id": "7", "group": "Carnes e ingredientes de origem animal", "examples": ["bovina", "suína", "aves", "cordeiro", "vísceras", "bacon", "banha", "gelatina"]},
    {"id": "8", "group": "Temperos, vegetais, sabores e texturas", "examples": ["alho", "cebola", "coentro", "salsa", "aipo", "pimenta", "cogumelos", "frutas", "comida crua", "pedaços ou sementes"]},
    {"id": "9", "group": "Modo de comer e outras escolhas", "examples": ["vegetariano", "vegano", "costume religioso", "menos sal", "menos açúcar", "menos gordura", "algum ingrediente não citado"]},
    {"id": "10", "group": "Produtos prontos e misturas", "examples": ["caldo em cubo", "tempero pronto", "molhos", "embutidos", "conservas", "corantes", "adoçantes", "outros aditivos"]},
)


def first_message() -> str:
    lines = [
        "O que devo evitar na sua comida?",
        "",
        "Pode responder com os números e os nomes, por escrito ou por voz, se estiver disponível. Se nenhum se aplica, diga “nenhum”; se tiver dúvida, diga “não sei”.",
        "",
    ]
    lines.extend(f"{item['id']}. **{item['group']}:** {', '.join(item['examples'])}." for item in CHECKLIST)
    lines.extend([
        "",
        "Para o item escolhido, diga o motivo que já conhece: alergia, intolerância, orientação alimentar, costume ou só não gostar. Não precisa contar diagnóstico. Se não souber, eu pergunto só o necessário.",
        "Escolher um grupo não exclui todos os exemplos e não indica um diagnóstico. Diga quais itens se aplicam a você.",
        "",
        "Exemplo: “1: não posso usar lactose; 7: não gosto de carne suína; 8: sem coentro”. Você também pode dizer outro ingrediente ou pedir que eu leia um grupo por vez.",
    ])
    return "\n".join(lines)


def onboarding_questions() -> dict:
    """Oferece o texto inicial pronto e campos para os hosts que usam JSON."""
    return {
        "first_message": first_message(),
        "checklist": [{**item, "examples": list(item["examples"])} for item in CHECKLIST],
        "reply_options": ["nenhum", "não sei", "números e nomes", "resposta livre", "um grupo por vez"],
        "host_instruction": "Mostre first_message diretamente, adaptando somente os itens já respondidos. Não abra com versão, ferramentas ou relatórios técnicos. Não trate um grupo marcado como diagnóstico nem como exclusão de todos os exemplos.",
        "questions": [
            {"field": "excluded_ingredients", "question": "Deste checklist, quais ingredientes devem ficar fora, por qualquer motivo? Pode indicar os nomes; marcar um grupo não exclui automaticamente todos os exemplos."},
            {"field": "allergies", "question": "Algum item é evitado por alergia já conhecida, como leite, ovo, amendoim, castanhas, peixe ou camarão? Informe só o ingrediente ou nenhum/não sei."},
            {"field": "intolerances", "question": "Algum item é evitado por intolerância já conhecida, como lactose? Informe só o ingrediente ou nenhum/não sei."},
            {"field": "preferences", "question": "Quais outros ingredientes não gosta ou prefere evitar, como coentro, pimenta ou vísceras? Informe os nomes; eles também serão excluídos deste pedido."},
            {"field": "equipment", "question": "O que pode usar: fogão, panela comum, panela de pressão, forno, air fryer, micro-ondas, liquidificador ou outro?"},
            {"field": "region", "question": "Deseja informar uma região culinária ampla? Não é necessário endereço; pode deixar em branco."},
            {"field": "servings", "question": "Para quantas pessoas ou porções deseja preparar?"},
            {"field": "language_style", "question": "Prefere explicação simples ou técnica?"},
            {"field": "onboarding_confirmed", "question": "Confirma as informações que escolheu informar para este pedido? Responda sim ou não."},
        ],
        "kitchen_checklist": [
            {"field": "dish", "question": "Já escolheu o prato ou quer sugestões com o que tem?"},
            {"field": "available_ingredients", "question": "O que tem em casa e quer aproveitar? Pode enviar uma lista ou, se disponível, uma foto para eu conferir com você."},
            {"field": "time_available_minutes", "question": "Quanto tempo pode esperar no total? Exemplo: 30 minutos, 1 hora ou posso começar hoje para servir amanhã."},
            {"field": "budget", "question": "Há um limite de gasto? Exemplo: até R$ 40 para quatro pessoas; pode dizer que não sabe."},
            {"field": "shopping_allowed", "question": "Pode comprar algum ingrediente que faltar ou precisa usar só o que tem?"},
            {"field": "taste_goal", "question": "Quer um resultado mais encorpado, aromático, fresco, suave, crocante ou outro?"},
            {"field": "output_mode", "question": "Prefere a receita inteira ou uma etapa de cada vez enquanto cozinha?"},
        ],
        "flavor_preference": "O preparo parte de ingredientes e técnicas, sem acrescentar realçador de sabor comercial. Confirme as demais escolhas sem presumir condição de saúde.",
        "alcohol_free_default": True,
        "privacy": "O servidor não persiste perfis. O host pode ter sua própria política de histórico.",
        "next_step": "Aproveite as respostas existentes e pergunte apenas o que falta. Confirme o prato e resolva nomes ambíguos com ingredientes distintivos antes de pesquisar.",
    }
