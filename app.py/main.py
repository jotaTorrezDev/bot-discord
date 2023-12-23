import discord
from discord.ext import commands, tasks

# Configuração do bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Lista de mensagens de divulgação
mensagens_divulgacao = [
    "Confira nosso servidor!", #Aqui vai a mensagem que voce quer que o bot envie!!
    
    
]

# Variável para rastrear se a tarefa de divulgação está ativa
divulgacao_ativa = False

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@tasks.loop(seconds=15)
async def divulgar():
    if divulgacao_ativa:
        # Itera sobre todas as mensagens de divulgação
        for mensagem in mensagens_divulgacao:
            # Itera sobre todos os servidores do bot
            for guild in bot.guilds:
                # Envia mensagens de divulgação nas DMs dos membros
                for member in guild.members:
                    try:
                        await member.send(mensagem)
                    except discord.Forbidden:
                        continue
                    except Exception as e:
                        print(f"Erro ao enviar mensagem para {member.name}: {e}")

                # Envia mensagens de divulgação em canais específicos nos servidores
                canal_divulgacao = discord.utils.get(guild.channels, name='geral')
                if canal_divulgacao:
                    try:
                        await canal_divulgacao.send(mensagem)
                    except discord.Forbidden:
                        continue
                    except Exception as e:
                        print(f"Erro ao enviar mensagem no canal de divulgação em {guild.name}: {e}")

@bot.command()
async def send_dm_to_all(ctx, server_id: int, *, message: str):
    try:
        # Obtenha o objeto do servidor usando o ID fornecido
        server = await bot.fetch_guild(server_id)

        # Verifique se o bot está no servidor
        if server and server.me:
            # Aguarde a coroutine fetch_members() antes de chamar flatten()
            members = await server.fetch_members().flatten()

            # Envia mensagens para todos os membros do servidor
            for member in members:
                try:
                    await member.send(message)
                except discord.Forbidden:
                    print(f"Não foi possível enviar mensagem para {member.name}. Permissões insuficientes.")
                except Exception as e:
                    print(f"Erro ao enviar mensagem para {member.name}: {e}")

            await ctx.send(f"Mensagens enviadas para todos os membros do servidor {server.name}.")
        else:
            await ctx.send("ID do servidor inválido ou o bot não está presente no servidor.")

    except Exception as e:
        print(f"Erro ao processar o comando: {e}")

# Comando para iniciar a tarefa de divulgação
@bot.command()
async def iniciardivulgacao(ctx):
    global divulgacao_ativa
    if not divulgacao_ativa:
        divulgar.start()
        divulgacao_ativa = True
        await ctx.send("Bem-vindo!")
    else:
        await ctx.send("A tarefa de divulgação já está em execução.")

# Comando para parar a tarefa de divulgação
@bot.command()
async def parardivulgacao(ctx):
    global divulgacao_ativa
    if divulgacao_ativa:
        divulgar.stop()
        divulgacao_ativa = False
        await ctx.send("Até mais!")
    else:
        await ctx.send("A tarefa de divulgação não está em execução.")

# Comando para atualizar a lista de mensagens de divulgação
@bot.command()
async def atualizardivulgacao(ctx, *, nova_mensagem: str):
    global mensagens_divulgacao
    mensagens_divulgacao.append(nova_mensagem)
    await ctx.send("As mensagens de divulgação foram atualizadas!")

# Substitua 'TOKEN_DO_SEU_BOT' pelo token real do seu bot
bot.run('Token do seu bot') #esse token voce pega no site do Discord Developer
