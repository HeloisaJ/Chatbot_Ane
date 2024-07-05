# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime, date, time, timedelta
import logging
from rasa_sdk.events import SlotSet,ReminderScheduled, ReminderCancelled
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import FormValidationAction

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""


    def name(self) -> Text:
        return "action_set_reminder"


    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        resp = tracker.get_slot("lembreteSet")
        tipo = tracker.get_slot("tipoLembrete")
        if(resp == False and tipo != None):
            #Obtendo stots
            number = next(tracker.get_latest_entity_values("number"), "no")
            time = next(tracker.get_latest_entity_values("time"), "no")
            hora = next(tracker.get_latest_entity_values("hora"), "no")

            if time == 'no':
                dispatcher.utter_message("Não esqueça de informar em quanto tempo você deseja receber o lembrete!")
                return []
            elif (time == 'minutos') or (time == 'minuto'):
                date = datetime.now() + timedelta(minutes=int(number))
                dispatcher.utter_message("Ok! Irei te enviar um lembrete em "+number+" "+time+".")
            elif (time == 'horas') or (time == 'hora'):
                date = datetime.now() + timedelta(hours=int(number))
                dispatcher.utter_message("Ok! Irei te enviar um lembrete em "+number+" "+time+".")
            elif (time =='dia'):
                day = number.split("/")
                print(hora)
                if hora == 'no':
                    date = datetime(datetime.now().year,int(day[1]),int(day[0]))
                    print(str(datetime.now().year)+"-"+str(day[1])+"-"+str(day[0]))
                    dispatcher.utter_message("Ok! Irei te enviar um lembrete no dia "+number+".")
                else:
                    horas = hora.split(":")
                    date = datetime(datetime.now().year,int(day[1]),int(day[0]),int(horas[0]),int(horas[1]))
                    print(str(datetime.now().year)+"-"+str(day[1])+"-"+str(day[0])+"-"+horas[0]+"-"+horas[1])
                    dispatcher.utter_message("Ok! Irei te enviar um lembrete no dia "+number+" as "+hora+" horas.")
            #segundos
            else:
                date = datetime.now() + timedelta(seconds=int(number))
                dispatcher.utter_message("Ok! Irei te enviar um lembrete em "+number+" "+time+".")

            dispatcher.utter_message("Digite retornar para o menu principal para acessar as diversas funcionalidades da Ane !")
            entities = tracker.latest_message.get("entities")

            reminder = ReminderScheduled(
                "EXTERNAL_reminder",
                trigger_date_time=date,
                entities=entities,
                name="my_reminder",
                kill_on_user_message=False,
            )

            evt = SlotSet(key = "lembreteSet", value = True)
            return [reminder, evt]
        elif(resp == False and tipo == None):
            dispatcher.utter_message(text="Pelo visto você não selecionou qual tipo de lembrete você prefere ! Selecione a parte de dicas do menu inicial para escolher e criar o seu lembrete!")
            return []
        else:
            dispatcher.utter_message(text="Pelo visto você já fez um lembrete, que ótimo! Mas você só pode criar um lembrete por vez, digite retornar para o menu inicial para ver o que mais temos para você !")
            return []

class ActionReactToReminder(Action):
    """Reminds the user to call someone."""


    def name(self) -> Text:
        return "action_react_to_reminder"


    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        tipo = tracker.get_slot("tipoLembrete")

        if(tipo == 'fisico'):
            dispatcher.utter_message(text="Mantenha-se ativo e faça pausas regulares ao usar a internet! Lembre-se de que atividades físicas podem ajudar a melhorar seu bem-estar físico e mental. Que tal definir uma meta de exercício para esta semana e ganhar uma recompensa ao final dela? Seu corpo e mente agradecem!")
        elif(tipo == 'mental'):
            dispatcher.utter_message(text="Mantenha sua mente saudável e equilibrada! Aproveite agora para dar uma pausa nas suas atividades online e fazer algo que te dê prazer e relaxe sua mente, como ler um livro, meditar, ouvir música ou praticar exercícios. Quando você se cuida, sua mente se fortalece e você se torna mais capaz de lidar com as demandas da vida online e offline. Experimente agora mesmo e sinta a diferença!")
        elif(tipo == 'cognitivo'):
            dispatcher.utter_message(text="Pequenas mudanças podem fazer uma grande diferença para o seu bem-estar cognitivo! Invista em momentos de descanso durante o uso da internet, pratique  meditação  e faça pausas regulares. Você está no caminho certo para um cérebro mais saudável e produtivo")
        elif(tipo == 'social'):
            dispatcher.utter_message(text="Você sabia que manter contato com seus amigos e familiares pode melhorar significativamente seu bem-estar social? Que tal planejar uma atividade social, como um jantar ou uma caminhada no parque, com seus entes queridos esta semana? Além de se divertir e criar boas memórias juntos, você estará fortalecendo seus relacionamentos e cuidando do seu bem-estar social.")
        else:
            dispatcher.utter_message(text="Você merece se sentir bem emocionalmente. Que tal reservar alguns minutos do seu dia para se desconectar da internet e se concentrar em atividades que tragam alegria e relaxamento, como ler um livro, ouvir música ou praticar uma atividade física? Aproveite para se reconectar consigo mesmo e recarregar suas energias emocionais.")

        evt1 = SlotSet(key = "lembreteSet", value = False)
        evt2 = SlotSet(key = "tipoLembrete", value = None)

        return [evt1, evt2]

class ForgetReminders(Action):
    """Cancels all reminders."""


    def name(self) -> Text:
        return "action_forget_reminders"


    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:


        dispatcher.utter_message("Ok, lembrete cancelado.")
        evt1 = SlotSet(key = "lembreteSet", value = False)
        evt2 = SlotSet(key = "tipoLembrete", value = None)

        # Cancel all reminders
        return [ReminderCancelled(), evt1, evt2]

class MyFallback(Action):

    def name(self) -> Text:
        return "action_my_fallback"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response = "utter_fallback")
        return []

class ActionAutorregulacao1(Action): # utter_motivacao affirm

    def name(self) -> Text:
        return "action_autorregulacao_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Experimente limitar seu tempo online e inclua outras atividades em sua rotina diária para ajudar a melhorar sua cognição e desempenho acadêmico.")
        dispatcher.utter_message(text= "Uma boa dica para o usuário que deseja gerenciar melhor seu tempo na internet é procurar um aplicativo de gerenciamento de tempo de sua preferência. Existem diversas opções disponíveis nas lojas de aplicativos, com diferentes recursos e funcionalidades, que podem ajudar o usuário a controlar o tempo gasto em cada atividade online e estabelecer metas para reduzir o uso excessivo. ")
        dispatcher.utter_message(text= "Com uma boa gestão do tempo, você reduzirá sua vulnerabilidade às redes sociais e à internet, além de ter mais tempo para se concentrar em suas atividades de estudo e trabalho. Dessa forma, é possível aumentar a produtividade e ter uma rotina mais equilibrada, com espaço para o lazer e o autocuidado.")
        dispatcher.utter_message(text= "Para ver mais opções, digite retornar ao menu principal.")

        return []

class ActionAutorregulacao2(Action): # utter_motivacao deny 2

    def name(self) -> Text:
        return "action_autorregulacao_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "É importante manter uma rotina de estudo, trabalho e lazer, estabelecendo horários específicos para essas atividades.")
        dispatcher.utter_message(text= "Além disso, é muito importante evitar o uso excessivo da internet e das redes sociais, principalmente durante suas atividade de trabalho, estudo e lazer.")
        dispatcher.utter_message(text= "As pausas regulares durante as atividades para descansar são importantes para evitar a sobrecraga mental.")
        dispatcher.utter_message(text= "Utilize ferramentas de gerenciamento do tempo para te auxiliar neste processo ou faça anotações em papel, por exemplo, em um planner ou agenda. Eles são muito úteis!")
        dispatcher.utter_message(text= "Não esqueça de praticar atividades físicas ou algum hobbie, eles podem te ajudar a manter o corpo e a mente saudável.")
        dispatcher.utter_message(text= "Para ver mais opções, digite retornar ao menu principal.")

        return []

class ActionAutorregulacao3(Action): # utter_motivacao affirm 2

    def name(self) -> Text:
        return "action_autorregulacao_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Tente refletir o que tem causado desmotivação. Tente desacelerar um pouco. Evite passar muitas horas navegando na internet.")
        dispatcher.utter_message(text= "Você pode começar limitando um pouco o tempo de uso da internet e estabelecer os horários específicos para acessá-la.")
        dispatcher.utter_message(text= "Considere procurar ajuda de um profissional caso a desmotivação continue afetando.")
        dispatcher.utter_message(text= "Para ver mais opções, digite retornar ao menu principal.")

        return []

class ActionAutorregulacao4(Action): # utter_tentou_limitar deny

    def name(self) -> Text:
        return "action_autorregulacao_4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Mesmo que não sinta a necessidade de limitar o seu tempo on-line, tente diminui-lo gradativamente e inclua outras atividades em sua rotina diária para ajudar a melhorar o seu bem-estar.")
        dispatcher.utter_message(text= "Procure ajuda profissional se continuar a ter dificuldades de concentração ou memória.")
        dispatcher.utter_message(text= "Para ver mais opções, digite retornar ao menu principal.")

        return []

class ActionAutorregulacao5(Action): # utter_tentou_limitar affirm

    def name(self) -> Text:
        return "action_autorregulacao_5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Continue limitando seu tempo online e incluindo outras atividades em sua rotina diária para ajudar a melhorar sua cognição.")
        dispatcher.utter_message(text= "Tente experimentar atividades no off-line. Pode ser uma ótima oportunidade de desenvolver alguma habilidade, como esporte.")
        dispatcher.utter_message(text= "Se você já tentou limitar seu tempo online e não conseguiu, pode ser útil buscar ajuda profissional que possa ajudá-lo a desenvolver estratégias para lidar com o uso problemático da internet e outras questões relacinadas.")
        dispatcher.utter_message(text= "Para ver mais opções, digite retornar ao menu principal.")

        return []

class ActionAutorregulacao6(Action): # utter_efeito_na_vida deny

    def name(self) -> Text:
        return "action_autorregulacao_6"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Parabéns! Continue a usar a internet com moderação e inclua outras atividades em sua rotina diária para manter um equilíbrio saudável.")
        dispatcher.utter_message(text= "Atividades ao ar livre são ótimas para o bem-estar pessoal. Você pode fazer exercícios, ler um livro ou passar tempo com amigos e familiares.")
        dispatcher.utter_message(text= "Para ver mais opções, digite retornar ao menu principal.")

        return []

class ActionAutocontrole1(Action): # utter_tempo_na_internet deny

    def name(self) -> Text:
        return "action_autocontrole_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Parabéns! O uso saudável da internet é importante e você parece estar no caminho certo.")
        dispatcher.utter_message(text= "É importante estar ciente de que o uso excessivo da internet pode levar a problemas de saúde mental e física, como ansiedade, depressão, obesidade e problemas de visão. É importante equilibrar o uso da internet com outras atividades saudáveis. Você pode considerar aprender coisas novas, como se conectar com outras pessoas, se divertir ou estudar. Depois, pense em objetivos mais específicos dentro dessas categorias. Por exemplo, se você quer aprender coisas novas, um objetivo específico poderia ser assistir um vídeo para aprender um novo idioma toda semana. ")
        dispatcher.utter_message(text= "Quer ver mais conteúdo ? Digite retornar ao menu principal e veja o que mais te espera.")

        return []

class ActionDicas1(Action): # Dicas bem-estar fisico

    def name(self) -> Text:
        return "action_dicas_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Faça pausas regulares: É importante levantar-se e fazer uma pausa a cada 30 minutos ou 1 hora de uso contínuo da internet. Movimente-se, alongue-se ou simplesmente caminhe um pouco pela casa.")
        dispatcher.utter_message(text= "Mantenha uma postura adequada: A má postura durante o uso de dispositivos eletrônicos pode causar dores nas costas, no pescoço e nos ombros. Mantenha a tela na altura dos olhos e use uma cadeira confortável com apoio para as costas.")
        dispatcher.utter_message(text= "Proteja seus olhos: A exposição excessiva à luz azul emitida pelas telas pode causar fadiga ocular e prejudicar o sono. Use o modo noturno ou o filtro de luz azul do dispositivo e faça pausas regulares para descansar os olhos.")
        dispatcher.utter_message(text= "Controle o tempo de tela: O uso excessivo da internet pode afetar negativamente a qualidade do sono e causar problemas de saúde. Defina limites para o tempo de tela e desligue os dispositivos eletrônicos pelo menos uma hora antes de dormir.")
        dispatcher.utter_message(text= "Pratique atividades físicas: O sedentarismo é um problema comum relacionado ao uso excessivo da internet. Pratique atividades físicas regularmente para manter a saúde física e mental.")
        dispatcher.utter_message(text= "Depois de todas essas dicas, que tal começar a aplicá-las no seu dia a dia. Aceita o convite ?")

        resp = tracker.get_slot("tipoLembrete")
        if(resp == None):
            evt = SlotSet(key = "tipoLembrete", value = "fisico")
            return [evt]
        return []

class ActionDicas2(Action): # Dicas bem-estar mental

    def name(self) -> Text:
        return "action_dicas_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Faça pausas regulares: Reserve um tempo para desconectar da internet e fazer outras atividades que você goste, como ler um livro, praticar exercícios físicos ou passar tempo com amigos e familiares.")
        dispatcher.utter_message(text= "Defina limites de tempo: Estabeleça um limite de tempo para usar a internet e siga-o. Se necessário, use aplicativos de gerenciamento de tempo para ajudá-lo a controlar quanto tempo você gasta em sites e aplicativos.")
        dispatcher.utter_message(text= "Evite conteúdo negativo: A exposição a conteúdo negativo, como notícias ruins ou imagens violentas, pode afetar negativamente sua saúde mental. Considere limitar sua exposição a esse tipo de conteúdo.")
        dispatcher.utter_message(text= "Pratique mindfulness: Práticas de mindfulness, como meditação e respiração consciente, podem ajudar a acalmar a mente e reduzir a ansiedade relacionada ao uso da internet.")
        dispatcher.utter_message(text= "Procure ajuda se necessário: Se você estiver sofrendo de problemas de saúde mental relacionados ao uso da internet, não hesite em procurar ajuda profissional. Terapia e aconselhamento podem ser úteis para lidar com questões como ansiedade, depressão e vício em tecnologia.")
        dispatcher.utter_message(text= "Depois de todas essas dicas, que tal começar a aplicá-las no seu dia a dia. Aceita o convite ?")

        resp = tracker.get_slot("tipoLembrete")
        if(resp == None):
            evt = SlotSet(key = "tipoLembrete", value = "mental")
            return [evt]
        return []

class ActionDicas3(Action): # Dicas bem-estar cognitivo

    def name(self) -> Text:
        return "action_dicas_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Defina um tempo limite para o uso da internet: Estabeleça limites diários e semanais para o uso da internet, seja para trabalhar ou para fins pessoais. Isso ajudará a evitar o esgotamento cognitivo e a sobrecarga de informações.")
        dispatcher.utter_message(text= "Faça pausas regulares: Faça pausas regulares ao longo do dia para se desconectar e descansar a mente. Use esse tempo para se mover, fazer exercícios de respiração ou meditação, ler um livro ou fazer algo criativo.")
        dispatcher.utter_message(text= "Selecione conteúdo relevante: Concentre-se em conteúdo relevante e valioso para suas necessidades e objetivos, evitando a sobrecarga de informações inúteis. Além disso, alguns conteúdos podem ser sensíveis á algumas pessoas e pode levar a emoções negativas.")
        dispatcher.utter_message(text= "Desative notificações: Desative as notificações desnecessárias em seu telefone e computador para minimizar as interrupções e manter o foco no trabalho ou nas atividades pessoais.")
        dispatcher.utter_message(text= "Pratique uma tarefa por vez: Tente evitar a multitarefa excessiva, pois ela pode levar à perda de produtividade e à sobrecarga cognitiva. Ao realizar várias tarefas simultaneamente, faça pausas frequentes e tente se concentrar em uma tarefa de cada vez.")
        dispatcher.utter_message(text= "Depois de todas essas dicas, que tal começar a aplicá-las no seu dia a dia. Aceita o convite ?")

        resp = tracker.get_slot("tipoLembrete")
        if(resp == None):
            evt = SlotSet(key = "tipoLembrete", value = "cognitivo")
            return [evt]
        return []

class ActionDicas4(Action): # Dicas bem-estar social

    def name(self) -> Text:
        return "action_dicas_4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "O primeiro passo para alcançar o bem-estar social é definir limites para o tempo de uso da internet e reserve tempo para atividades sociais off-line, como sair com os amigos ou praticar algum hobbie.")
        dispatcher.utter_message(text= "Use a internet para se conectar com amigos e familiares, mas não deixe que ela substitua as interações sociais face a face.")
        dispatcher.utter_message(text= "Seja seletivo em relação às redes sociais que você usa e as pessoas que segue. Siga aqueles que compartilham conteúdo positivo e que o inspiram.")
        dispatcher.utter_message(text= "Não deixe que as redes sociais o levem a fazer comparações negativas com os outros. Lembre-se de que muitas vezes as pessoas só compartilham suas melhores experiências e isso pode criar uma imagem irreal do que é a vida.")
        dispatcher.utter_message(text= "Depois de todas essas dicas, que tal começar a aplicá-las no seu dia a dia. Aceita o convite ?")


        resp = tracker.get_slot("tipoLembrete")
        if(resp == None):
            evt = SlotSet(key = "tipoLembrete", value = "social")
            return [evt]
        return []

class ActionDicas5(Action): # Dicas bem-estar emocional

    def name(self) -> Text:
        return "action_dicas_5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Quando você sente que suas emoções estão ficando fora de controle enquanto navega na internet, é importante se afastar da tela e praticar a autorregulação emocional. Isso pode incluir técnicas como respiração profunda, meditação ou simplesmente fazer uma pausa e fazer algo relaxante, como ouvir música.")
        dispatcher.utter_message(text= "É importante definir limites saudáveis para o uso da internet e aderir a eles. Por exemplo, estabeleça um horário específico para usar a internet e tente se afastar de todas as telas pelo menos uma hora antes de dormir. Isso pode ajudar a promover um sono melhor e reduzir o estresse relacionado ao uso excessivo da internet.")
        dispatcher.utter_message(text= "Cultive relacionamentos offline: Embora a internet possa ser uma ótima ferramenta para se conectar com os outros, é importante cultivar relacionamentos fora da tela. Tente se conectar com amigos e familiares em pessoa e passar mais tempo participando de atividades que não envolvam o uso da internet. Isso pode ajudá-lo a se sentir mais equilibrado e conectado.")
        dispatcher.utter_message(text= "Depois de todas essas dicas, que tal começar a aplicá-las no seu dia a dia. Aceita o convite ?")

        resp = tracker.get_slot("tipoLembrete")
        if(resp == None):
            evt = SlotSet(key = "tipoLembrete", value = "emocional")
            return [evt]
        return []

class ActionLembretes1(Action): # Lembretes bem-estar fisico

    def name(self) -> Text:
        return "action_lembretes_1"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Parabéns por começar a cuidar do seu bem-estar digital! Lembre-se de fazer pausas frequentes e manter uma boa postura para evitar dores físicas.")
        dispatcher.utter_message(text= "Você deseja definir lembretes ?")

        return []

class ActionLembretes2(Action): # Lembretes bem-estar mental

    def name(self) -> Text:
        return "action_lembretes_2"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Parabéns por tomar medidas para cuidar da sua saúde mental. Lembre-se de sempre verificar como as atividades online afetam sua mente e bem-estar emocional.")
        dispatcher.utter_message(text= "Você deseja definir lembretes ?")

        return []

class ActionLembretes3(Action): # Lembretes bem-estar cognitivo

    def name(self) -> Text:
        return "action_lembretes_3"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Parabéns por dar o primeiro passo para cuidar da sua saúde cognitiva. Lembre-se de praticar multitarefa consciente e fazer pausas frequentes para descansar sua mente.")
        dispatcher.utter_message(text= "Você deseja definir lembretes ?")

        return []

class ActionLembretes4(Action): # Lembretes bem-estar social

    def name(self) -> Text:
        return "action_lembretes_4"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Parabéns por dar o primeiro passo para cuidar da sua saúde social. Lembre-se de verificar como as suas interações online afetam suas relações pessoais.")
        dispatcher.utter_message(text= "Você deseja definir lembretes ?")

        return []

class ActionLembretes5(Action): # Lembretes bem-estar fisico

    def name(self) -> Text:
        return "action_lembretes_5"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Parabéns por dar o primeiro passo para cuidar da sua saúde emocional digital. Lembre-se de verificar como as atividades online afetam suas emoções e sentimentos.")
        dispatcher.utter_message(text= "Você deseja definir lembretes ?")

        return []

class ActionSetLembretes(Action): # Lembretes bem-estar fisico

    def name(self) -> Text:
        return "action_set_lembretes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        resp = tracker.get_slot("lembreteSet")
        if(resp == False):
            dispatcher.utter_message(text="Ok, quando você quer receber este lembrete ? Ex: Me envie um lembrete no dia 02/12 as 12:00 horas !")
        else:
            dispatcher.utter_message(text="Pelo visto você já fez um lembrete, que ótimo! Mas você só pode criar um lembrete por vez, digite retornar para o menu inicial para ver o que mais temos para você !")

        return []

class ActionConviteDeny(Action):

    def name(self) -> Text:
        return "action_convite_deny"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Tudo bem. Lembre-se de que estou aqui para navegar junto com você em busca de soluções. Sinta-se à vontade para me chamar sempre que precisar. Para voltar ao menu principal digite: voltar ao menu, até logo! :)")
        evt = SlotSet(key = "tipoLembrete", value = None)
        return [evt]

class ActionLembreteDeny(Action):

    def name(self) -> Text:
        return "action_lembrete_deny"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text= "Fico feliz em saber que posso ser útil. Quando você estiver pronto(a) para receber lembretes, é só me chamar. Para voltar ao menu principal digite: voltar ao menu, estarei aqui para ajudar no que for preciso. Até logo! :)")
        evt = SlotSet(key = "tipoLembrete", value = None)
        return [evt]

class ActionQuestionario(Action):

    def name(self) -> Text:
        return "action_questionario"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       resp = tracker.get_slot("quest")

       if(resp == "Até 2h"):
           dispatcher.utter_message(text= "Parabéns por ter um bom equilíbrio entre o uso da internet e outras atividades! Continue assim e lembre-se de sempre buscar um estilo de vida saudável e equilibrado.")
       elif(resp == "Entre 2h e 4h"):
           dispatcher.utter_message(text= "Parabéns por ter um controle moderado do tempo de uso da internet! Você está dentro dos padrões. Mas lembre-se de manter o equilíbrio e sempre buscar outras atividades para complementar o seu tempo livre.")
           dispatcher.utter_message(text= "Tente estabelecer horários para o uso da internet e limite o tempo gasto em redes sociais e aplicativos; faça pausas regulares para alongar o corpo, descansar os olhos e se desconectar da tela; busque atividades offline para fazer com amigos e familiares, como sair para passear ou jogar algum jogo de tabuleiro.")
       else:
           dispatcher.utter_message(text= "Procure ajuda de um profissional para avaliar se há uma dependência do uso da internet e buscar formas de controlar o comportamento; tente reduzir gradualmente o tempo gasto na internet e substituir por outras atividades que lhe proporcionem prazer e bem-estar; evite usar a internet antes de dormir e estabeleça horários para o uso das redes sociais.")
           dispatcher.utter_message(text= "Buscar ajuda e reconhecer que há um problema já é um passo importante para superar a dependência do uso da internet. Parabéns por estar buscando soluções para melhorar a qualidade de vida e controlar o comportamento. Lembre-se de que é possível superar essa dificuldade com esforço, dedicação e apoio de pessoas próximas.")

       dispatcher.utter_message(text= "Quer ver mais conteúdo ? Digite retornar ao menu principal e veja o que mais te espera.")

       return []
