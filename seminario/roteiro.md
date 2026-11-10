# Roteiro: Belief Control Barrier Functions (~15 min)

Tempo total previsto: **14:45**. O tempo ao lado de cada slide é quanto falar nele; o valor entre colchetes é o acumulado ao terminar o slide.

| Bloco | Slides | Tempo |
|---|---|---|
| Abertura | 1–3 | 1:30 |
| CBF clássica | 4–8 | 4:30 |
| Restrições de chance e VaR | 9–11 | 2:45 |
| Método (BCBF) | 12–15 | 3:30 |
| Resultados | 16–17 | 1:45 |
| Conclusão | 18–19 | 0:45 |

---

## Abertura

### Slide 1 — Capa · 0:15 [0:15]
> Boa tarde. Vou apresentar o artigo *Belief Control Barrier Functions for Risk-Aware Control*, de Vahs, Pek e Tumova, publicado na RA-L em 2023.

### Slide 2 — Agenda · 0:15 [0:30]
> Primeiro vou explicar o que são Control Barrier Functions, que é a base de tudo. Depois, como tratar segurança quando o estado é incerto, com restrições de chance e VaR. Aí entro no método do artigo, nos resultados e fecho com a conclusão.

### Slide 3 — Motivação · 1:00 [1:30]
> Robôs reais lidam com ruído de sensores e perturbações, como o vento nesse quadrotor da figura. Por isso o robô nunca sabe exatamente onde está: o que ele tem é uma **crença**, uma média e uma covariância, vinda de um filtro como o EKF. Essa elipse roxa na figura é essa incerteza.
>
> O problema é que os controladores de segurança clássicos usam só a média e jogam fora a incerteza. O que o artigo quer é uma garantia do tipo: "a probabilidade de sair da região segura é menor que 1%".

**Transição:** "Para entender a proposta, preciso primeiro explicar a ferramenta clássica: as CBFs."

---

## CBF clássica

### Slide 4 — CBFs: Ideia Central · 0:50 [2:20]
> Considere um sistema afim no controle, ẋ = f(x) + g(x)u. A segurança é descrita por uma função h: onde h é maior ou igual a zero é seguro, e o conjunto C é essa região. A fronteira é onde h vale zero.
>
> O objetivo é a **invariância**: se o robô começa dentro de C, ele nunca sai. A trajetória pode até encostar na fronteira, como no desenho, mas não atravessa.

### Slide 5 — A Condição de Barreira · 1:10 [3:30]
> Como garantir isso? Olhando para a derivada de h ao longo do movimento. Ela tem uma parte que não depende do controle e uma parte linear em u.
>
> A condição de CBF diz: escolha u de forma que ḣ ≥ −γ h. A intuição é a seguinte:
> - **longe da fronteira**, h é grande e a restrição é frouxa: o robô faz o que quiser;
> - **na fronteira**, h é zero, então ḣ tem que ser ≥ 0: ele não pode avançar para fora;
> - **fora do conjunto**, a condição força ḣ positivo e o robô é empurrado de volta.
>
> Ou seja, h pode diminuir, mas cada vez mais devagar perto da borda. E o teorema garante que, com essa condição, C é invariante.

### Slide 6 — Filtro de Segurança via QP · 0:50 [4:20]
> Na prática, isso vira um filtro. Existe um controlador nominal, u_ref, que não sabe nada de segurança: pode ser um LQR, um operador humano, um planejador. A CBF resolve um QP que encontra o controle mais próximo possível de u_ref que respeite a condição.
>
> Como a restrição é linear em u, o problema é convexo e resolve em micro a milissegundos: **tempo real**. E se u_ref já for seguro, o filtro não mexe em nada.

### Slide 7 — Exemplo 1D · 1:00 [5:20]
> Um exemplo simples: um robô em 1D, com ẋ = u, e uma parede em x_max. A função é h = x_max − x, a distância até a parede.
>
> A condição de CBF vira u ≤ γ(x_max − x): a velocidade máxima em direção à parede diminui linearmente com a distância. A solução do QP é só o mínimo entre u_ref e esse limite.
>
> No gráfico: longe da parede, o robô anda na velocidade que quiser; perto dela, vai freando, e chega encostando sem bater.

### Slide 8 — Limitação · 0:40 [6:00]
> Só que tudo isso supõe que o **estado é conhecido exatamente**. Na prática, temos uma estimativa ruidosa. Se eu aplico a CBF na média, posso achar que estou seguro enquanto o robô real não está. E como o ruído é Gaussiano, não existe uma margem fixa que garanta segurança.
>
> A ideia do artigo é aplicar a CBF sobre a **crença**, a média e a covariância, e não sobre o estado.

**Transição:** "Para isso, primeiro precisamos definir o que é 'seguro' quando o estado é aleatório."

---

## Restrições de chance e VaR

### Slide 9 — Restrições de Chance · 0:50 [6:50]
> O EKF diz que o estado é uma Gaussiana com média μ e covariância Σ. A segurança é um semiespaço, αᵀx ≥ β, por exemplo ficar antes de uma parede.
>
> Como a Gaussiana tem suporte infinito, sempre há **alguma** chance de violação. Então não dá para exigir segurança com certeza; exigimos com alta probabilidade: Pr ≥ 1 − δ, onde δ é o risco que aceitamos. Com δ = 1%, o robô fica seguro em 99% dos casos. No gráfico, a área vermelha é a probabilidade de violação, e ela tem que ser no máximo δ.

### Slide 10 — Value-at-Risk · 1:05 [7:55]
> Para trabalhar com isso usamos o **Value-at-Risk**. O VaR é o quantil inferior da distribuição: o valor que y supera com probabilidade 1 − δ.
>
> Exemplo: y é a distância do robô até a parede, com média 1 m e desvio de 0,4 m, e δ = 5%. O quantil de 5% é 1 − 1,645 · 0,4 ≈ 0,34 m. Ou seja: **com 95% de chance, o robô está a pelo menos 34 cm da parede**. O VaR diz quanta margem de segurança temos para o risco escolhido.
>
> E a ligação com a restrição de chance é direta: se o VaR é não negativo, o risco de violação está dentro do limite.

### Slide 11 — VaR para Gaussianas · 0:50 [8:45]
> Para Gaussianas, o VaR tem forma fechada: é a média menos z_δ desvios-padrão. Os valores de z estão na tabela: 1,28 para 10%, 1,64 para 5%, 2,33 para 1%.
>
> Então a restrição de chance vira uma função da crença, h_b: a **distância da média até a fronteira** menos uma **margem proporcional à incerteza**. Quanto maior a incerteza ou menor o risco aceito, maior a margem.
>
> E o ponto chave: h_b é uma função **determinística** da crença. Então ela pode servir de CBF.

**Transição:** "E é exatamente isso que o artigo faz."

---

## Método (BCBF)

### Slide 12 — Conjunto Seguro Sobre Crenças · 0:50 [9:35]
> A restrição de chance define um conjunto seguro, só que agora no espaço das **crenças**. No exemplo do drone em 1D, com parede em x = 2 e 90% de confiança, h_b = 2 − μ − 1,28σ.
>
> No gráfico, o eixo horizontal é a média e o vertical é a variância. A região azul são as crenças seguras: quanto maior a variância, mais longe da parede a média precisa estar. No ponto vermelho, a probabilidade de colisão é exatamente 10%.

### Slide 13 — Sistema Híbrido · 0:50 [10:25]
> Para aplicar uma CBF, preciso saber como a crença evolui. E ela tem duas dinâmicas:
> - **entre medições**, a predição do EKF: contínua, determinística e afim no controle, a mesma forma das CBFs; a incerteza cresce;
> - **quando chega uma medição**, a atualização de Kalman: um salto instantâneo, e **aleatório**, porque a medição é ruidosa; a incerteza cai.
>
> No gráfico, a variância cresce, cai em cada medição, e se ficar muito tempo sem medição, como sem GPS, ela cresce bastante.

### Slide 14 — Belief Control Barrier Functions · 1:00 [11:25]
> A BCBF é exatamente a condição de CBF, só que aplicada à crença.
>
> Entre medições a crença é determinística, então vale a mesma garantia da CBF clássica: o conjunto é invariante. O problema é o salto: uma medição **outlier** pode fazer a crença pular para fora do conjunto seguro, mesmo com o robô real ainda seguro. É o que mostra a figura: b⁻ estava seguro e b⁺ saiu.
>
> O artigo limita a probabilidade desse salto e, como a CBF é assintoticamente estável, a crença é trazida de volta.

### Slide 15 — Margem de Segurança e Controle Final · 0:50 [12:15]
> Para evitar o salto, o artigo encolhe o conjunto seguro com uma margem γ. Com γ escolhido pelo Teorema 3, a probabilidade de continuar dentro do conjunto após cada medição é pelo menos 1 − ε.
>
> O controle final é o mesmo QP da CBF clássica, só que sobre a crença. Ele otimiza só sobre u, não sobre a crença, que é enorme (90 dimensões no quadrotor). Por isso continua em **tempo real**, até 1 kHz.

**Transição:** "Vamos ver se funciona."

---

## Resultados

### Slide 16 — Simulação · 0:55 [13:10]
> Na simulação, um uniciclo ruidoso precisa desviar de um obstáculo; são 100 trajetórias. Compararam com uma CBF estocástica e com um MPC com restrições de chance, o CCNMPC.
>
> A BCBF teve **zero colisões**, contra 3 dos outros dois métodos, e é cerca de 200 vezes mais rápida que o MPC. O custo é eficiência: as trajetórias do MPC são melhores, porque ele planeja no horizonte e a CBF é reativa.

### Slide 17 — Experimento Real · 0:50 [14:00]
> No experimento real, um Crazyflie voa num corredor em U em que o ruído e a taxa de medição mudam em cada trecho.
>
> A CBF baseada só na média **viola** a segurança. A BCBF fez **20 de 20 execuções seguras**. Um detalhe interessante: ela evita o trecho estreito da direita, porque o risco ali é alto demais, e contorna pela esquerda. Isso mostra o lado bom, ser consciente do risco, e o ruim: pode ficar presa em mínimos locais.

---

## Conclusão

### Slide 18 — Conclusão · 0:35 [14:35]
> Resumindo: a BCBF é uma CBF aplicada à crença do EKF. A segurança vira um limite na probabilidade de violação, com garantias mesmo com medições discretas e outliers, e continua sendo um QP em tempo real, aplicável a qualquer robô com EKF.
>
> As limitações: supõe crença Gaussiana, e os autores sugerem filtros de partículas como trabalho futuro; e, por ser reativa, pode ficar presa em mínimos locais, o que pediria combinar com MPC ou um planejador.

### Slide 19 — Obrigado · 0:10 [14:45]
> Obrigado. Fico à disposição para perguntas.

---

## Possíveis perguntas

- **Por que não usar MPC direto?** O MPC com restrições de chance é ~200× mais lento e às vezes fica inviável, precisando relaxar a restrição. A BCBF é um QP pequeno, sempre rápido.
- **E se a crença não for Gaussiana?** O VaR em forma fechada depende disso. Para crenças multimodais seria preciso outra formulação; os autores citam filtros de partículas como trabalho futuro.
- **O EKF não é aproximado?** Sim, em sistemas não lineares a crença Gaussiana é uma aproximação. As garantias valem para a crença modelada, não necessariamente para a distribuição real.
- **Qual a diferença entre δ e ε?** δ é o risco aceito para o **estado** sair do conjunto seguro. ε é o risco de a **crença** sair do conjunto seguro por causa de uma medição outlier.
- **O que é grau relativo?** Quando u não aparece na primeira derivada de h (ex.: controle por aceleração), deriva-se de novo; o artigo usa CBFs exponenciais de segunda ordem para isso.
