from ensurepip import version
import discord
from discord.ext import commands
import datetime
from discord.utils import get
import json
import random
import time
import sys
import os
import asyncio
import math
from core.classes import Cog_Extension
from io import StringIO
ver = "@party_game_bot 2022 Version 1.0.0 by:Ststone"
def read_file(filename:str):
    with open(filename+'.json','r',encoding='utf-8') as f:
        data = json.load(f)
    return data
def write_file(filename:str,data:dict):
    with open(filename+'.json','w',encoding='utf-8') as f:
        json.dump(data,f)

class Train(Cog_Extension):
    @commands.command(aliases=["重置遊戲","重置","重開","reset"],help="")
    async def reset_game(self,message):
        role1 = self.bot.get_guild(997548822148423771).get_role(997877192707022960)
        if(role1 not in message.author.roles):
            return
        write_file("player",{"list":[]})
        write_file("game",{})
        await message.channel.send("重置成功！")
    @commands.command(aliases=["加入遊戲","加入","參加","報名","join"],help="")
    async def join_game(self,message):
        lobby = self.bot.get_channel(997875993907834931)
        ID = str(message.author.id)
        CID = str(message.channel.id)
        ok = 1
        p_data = read_file("player")
        for i in p_data["list"]:
            if(ID==i):
                ok = 0
        if(ok):
            p_data["list"].append(ID)
            p_data[CID] = ID
            write_file("player",p_data)
            await message.channel.send("加入成功")
            await lobby.send("<@"+ID+">加入了遊戲")
        else:
            await message.channel.send("您已經加入遊戲了，若有疑慮，請告知管理員錯誤代碼a5fs7")
    @commands.command(aliases=["開始遊戲","遊戲開始","start"],help="")
    async def start_game(self,message):
        role1 = self.bot.get_guild(997548822148423771).get_role(997877192707022960)
        if(role1 not in message.author.roles):
            return
        lobby = self.bot.get_channel(997875993907834931)
        p_data = read_file("player")
        g_data = read_file("game")
        c_data = read_file("train/data")
        peo_data = c_data["people"]
        eve_data = c_data["event"]
        n = len(p_data["list"])
        if(n<3 or n>20):
            await message.channel.send("本遊戲目前只支援遊玩人數3~20人，若有疑慮，請告知管理員錯誤代碼a8hnd。")
            return
        try:
            if(g_data["start"]=="T"):
                await message.channel.send("遊戲已經開始ㄌ，若有疑慮，請告知管理員錯誤代碼ku6r9。")
                return
        except:
            pass
        g_data["type"] = "train"
        g_data["round"] = 0
        g_data["vote"] = []
        g_data["pc1"] = []
        g_data["pc2"] = []
        g_data["card_info"] = []
        g_data["card_choose"] = []
        g_data["player_info"] = []
        g_data["player"] = n
        g_data["cnt"] = 0
        g_data["score"] = []
        g_data["battle"] = []
        g_data["start"] = "T"
        for i in p_data["list"]:
            g_data["score"].append([i,0])
        for i in range(n):
            a = random.randint(0,n-1)
            p_data["list"][i],p_data["list"][a] = p_data["list"][a],p_data["list"][i]
        #print(p_data["list"])
        x,y = [],[]
        if(n%2==1):
            x.append(p_data["list"][int(n/2)])
        for i in range(int(n/2)):
            x.append(p_data["list"][i])
            x.append(p_data["list"][i])
            y.append(p_data["list"][n-1-i])
            y.append(p_data["list"][n-1-i])
        if(n%2==1):
            y.append(p_data["list"][int(n/2)])
        #print(x)
        #print(y)
        for i in range(len(x)):
            a = random.randint(0,len(x)-1)
            b = random.randint(0,len(y)-1)
            x[i],x[a] = x[a],x[i]
            y[i],y[b] = y[b],y[i]
        for i in range(len(x)):
            if(x[i]==y[i]):
                a = random.randint(0,len(x)-1)
                while(a==i):
                    a = random.randint(0,len(x)-1)
                x[i],x[a] = x[a],x[i]
        for i in range(len(x)):
            a = random.randint(0,1)
            if(a==1):
                g_data["battle"].append([x[i],y[i]])
            else:
                g_data["battle"].append([y[i],x[i]])
        for i in range(len(x)):
            w,z,pp1,pp2,usep = [],[],[],[],[]
            for i in range(3):
                peo1 = peo_data[random.randint(0,len(peo_data)-1)]
                while(peo1 in usep):
                    peo1 = peo_data[random.randint(0,len(peo_data)-1)]
                pp1.append(peo1)
                usep.append(peo1)
            for i in range(3):
                peo2 = peo_data[random.randint(0,len(peo_data)-1)]
                while(peo2 in usep):
                    peo2 = peo_data[random.randint(0,len(peo_data)-1)]
                pp2.append(peo2)
                usep.append(peo2)
            g_data["card_choose"].append([pp1,pp2])
            g_data["card_info"].append(["待選擇","待選擇"])
            for j in range(7):
                w.append(eve_data[random.randint(0,len(eve_data)-1)])
                z.append(eve_data[random.randint(0,len(eve_data)-1)])
            g_data["player_info"].append([w,z])
        write_file("game",g_data)
        embed = discord.Embed(title="比賽表",description="前方為先攻ㄉ人",color=0xeee657)
        for i in range(len(g_data["battle"])):
            show = "<@"+g_data["battle"][i][0]+"> vs. <@"+g_data["battle"][i][1]+">"
            embed.add_field(name="Round."+str(i+1), value=show, inline=False)
        embed.set_footer(text=ver)
        await lobby.send(embed=embed)
        ####same as now_info
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        R = g_data["round"]
        z = "Round."+str(R+1)+'\n'
        z += "<@"+g_data["battle"][R][0]+"> vs. <@"+g_data["battle"][R][1]+">"
        embed = discord.Embed(title="當前比賽狀況",description=z,color=0xeee657)
        x,y = "可是：","可是："
        for i in g_data["pc1"]:
            x += " ["+i+"] "
        for i in g_data["pc2"]:
            y += " ["+i+"] "
        embed.add_field(name="A鐵軌："+str(g_data["card_info"][R][0]), value=x, inline=False)
        embed.add_field(name="B鐵軌："+str(g_data["card_info"][R][1]), value=y, inline=False)
        embed.set_footer(text=ver)
        await lobby.send(embed=embed)
        ######
        await lobby.send("請雙方先選擇要保護的對象。")
    @commands.command(aliases=["比賽狀況","information"],help="")
    async def now_info(self,message):
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        R = g_data["round"]
        z = "Round."+str(R+1)+'\n'
        z += "<@"+g_data["battle"][R][0]+"> vs. <@"+g_data["battle"][R][1]+">"
        embed = discord.Embed(title="當前比賽狀況",description=z,color=0xeee657)
        x,y = "可是：","可是："
        for i in g_data["pc1"]:
            x += " ["+i+"] "
        for i in g_data["pc2"]:
            y += " ["+i+"] "
        embed.add_field(name="A鐵軌："+str(g_data["card_info"][R][0]), value=x, inline=False)
        embed.add_field(name="B鐵軌："+str(g_data["card_info"][R][1]), value=y, inline=False)
        embed.set_footer(text=ver)
        await lobby.send(embed=embed)
    @commands.command(aliases=["公布結果","公布","結果"],help="")
    async def result(self,message):
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        r_data = read_file("train/rating")
        R = g_data["round"]
        if(g_data["cnt"]!=6):
            await lobby.send("兩位玩家合計尚未出滿6張卡片。")
            return
        if(len(g_data["vote"])!=g_data["player"]-2):
            await lobby.send("還有玩家沒有進行投票。")
            return
        x,y = 0,0
        win = ""
        for i in range(g_data["player"]-2):
            if(g_data["vote"][i][0]=='A'):
                x += 1
            elif(g_data["vote"][i][0]=='B'):
                y += 1
        if(x>y):
            win = "B"
        elif(y>x):
            win = "A"
        else:
            win = "tie"
        if(win=="tie"):
            await lobby.send("本局結果："+str(x)+"票對"+str(y)+"票，平手。")
        elif(win=="A"):
            for i in range(len(g_data["score"])):
                if(g_data["score"][i][0]==g_data["battle"][R][0]):
                    g_data["score"][i][1] += y
            for i in range(g_data["player"]-2):
                if(g_data["vote"][i][0]=='B'):
                    for j in range(len(g_data["score"])):
                        if(g_data["score"][j][0]==g_data["vote"][i][1]):
                            g_data["score"][j][1] += x+1
        elif(win=="B"):
            for i in range(len(g_data["score"])):
                if(g_data["score"][i][0]==g_data["battle"][R][1]):
                    g_data["score"][i][1] += x
            for i in range(g_data["player"]-2):
                if(g_data["vote"][i][0]=='A'):
                    for j in range(len(g_data["score"])):
                        if(g_data["score"][j][0]==g_data["vote"][i][1]):
                            g_data["score"][j][1] += y+1
        g_data["round"] += 1
        g_data["cnt"] = 0
        g_data["vote"] = []
        g_data["pc1"] = []
        g_data["pc2"] = []
        write_file("game",g_data)
        if(x>y):
            await lobby.send("本局結果："+str(x)+"票對"+str(y)+"票，A將被火車輾過。")
        elif(y>x):
            await lobby.send("本局結果："+str(x)+"票對"+str(y)+"票，B將被火車輾過。")
        if(g_data["round"]==g_data["player"]):
            xx,yy,ww,ne = [],[],[],[]
            for i in g_data["score"]:
                xx.append(i[0])
            for i in xx:
                zz = []
                for j in xx:
                    aa,bb = 0,0
                    try:
                        aa = r_data[i][0]
                    except:
                        aa = 0
                    try:
                        bb = r_data[j][0]
                    except:
                        bb = 0
                    zz.append((aa+100)/(aa+bb+200))
                yy.append(zz)
            for i in range(len(xx)):
                zz = []
                for j in range(len(xx)):
                    if(g_data["score"][i][1]>=g_data["score"][j][1]):
                        zz.append(1)
                    else:
                        zz.append(0)
                ww.append(zz)
            #print(yy)
            #print(ww)
            for i in range(len(xx)):
                delta = 0
                for j in range(len(xx)):
                    aa,bb = 0,0
                    try:
                        aa = r_data[xx[i]][0]
                    except:
                        aa = 0
                    try:
                        bb = r_data[xx[j]][0]
                    except:
                        bb = 0
                    if(ww[i][j]==1 and i!=j and aa<100):
                        delta += min(max(int(abs(aa-bb)*(1-yy[i][j])*0.36787944117),10),111)
                    elif(ww[i][j]==1 and i!=j):
                        delta += min(int(abs(aa-bb)*(1-yy[i][j])*0.36787944117),111)
                    elif(ww[i][j]==0 and i!=j):
                        delta -= min(int(abs(aa-bb)*(yy[i][j])*0.36787944117),111)
                if(aa>=100 and aa-delta<100):
                    delta = aa-100
                elif(aa<100):
                    delta = max(delta,0)
                elif(aa==0):
                    delta = 1
                ne.append(delta)
            #print(ne)
            for i in range(len(xx)):
                try:
                    r_data[xx[i]] = [r_data[xx[i]][0]+ne[i],ne[i]]
                except:
                    r_data[xx[i]] = [0+ne[i],ne[i]]
            write_file("train/rating",r_data)
            await lobby.send("遊戲結束")
    @commands.command(aliases=["積分","排位"],help="")
    async def rating(self,message):
        ID = str(message.author.id)
        lobby = self.bot.get_channel(997875993907834931)
        r_data = read_file("train/rating")
        x = []
        for i in r_data.keys():
            x.append([-r_data[i][0],r_data[i][1],i])
        x = sorted(x)
        embed = discord.Embed(title="排位",description="排位系統",color=0xeee657)
        add = ""
        la = 1
        las = 8787878787
        for i in range(len(x)):
            if(-x[i][0]==-las):
                if(x[i][1]>=0):
                    add += "No."+str(la)+":<@"+x[i][2]+">:"+str(-x[i][0])+"(+"+str(x[i][1])+")\n"
                else:
                    add += "No."+str(la)+":<@"+x[i][2]+">:"+str(-x[i][0])+"("+str(x[i][1])+")\n"
            else:
                la = i+1
                if(x[i][1]>=0):
                    add += "No."+str(i+1)+":<@"+x[i][2]+">:"+str(-x[i][0])+"(+"+str(x[i][1])+")\n"
                else:
                    add += "No."+str(i+1)+":<@"+x[i][2]+">:"+str(-x[i][0])+"("+str(x[i][1])+")\n"
            las = x[i][0]
        embed.add_field(name="排行榜", value=add, inline=False)
        embed.set_footer(text=ver)
        await lobby.send(embed=embed)
    @commands.command(aliases=["投票","投"],help="")
    async def vote(self,message,who:str):
        ID = str(message.author.id)
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        R = g_data["round"]
        if(ID==g_data["battle"][R][0] or ID==g_data["battle"][R][1]):
            await message.channel.send("您無法投票！")
            return
        if(g_data["cnt"]!=6):
            await lobby.send("兩位玩家合計尚未出滿6張卡片，故還無法投票。")
            return
        ok = 1
        for i in g_data["vote"]:
            if(i[1]==ID):
                await lobby.send("您已經投過票了。")
                return
        if(who!='A' and who!='B'):
            await message.channel.send("投票時只能投給A或是B。")
            return
        g_data["vote"].append([who,ID])
        write_file("game",g_data)
        await message.channel.send("投票成功。")
        await lobby.send("<@"+ID+">完成了投票。")
        if(len(g_data["vote"])==g_data["player"]-2):
            #same as result
            lobby = self.bot.get_channel(997875993907834931)
            g_data = read_file("game")
            r_data = read_file("train/rating")
            R = g_data["round"]
            if(g_data["cnt"]!=6):
                await lobby.send("兩位玩家合計尚未出滿6張卡片。")
                return
            if(len(g_data["vote"])!=g_data["player"]-2):
                await lobby.send("還有玩家沒有進行投票。")
                return
            x,y = 0,0
            win = ""
            for i in range(g_data["player"]-2):
                if(g_data["vote"][i][0]=='A'):
                    x += 1
                elif(g_data["vote"][i][0]=='B'):
                    y += 1
            if(x>y):
                win = "B"
            elif(y>x):
                win = "A"
            else:
                win = "tie"
            if(win=="tie"):
                await lobby.send("本局結果："+str(x)+"票對"+str(y)+"票，平手。")
            elif(win=="A"):
                for i in range(len(g_data["score"])):
                    if(g_data["score"][i][0]==g_data["battle"][R][0]):
                        g_data["score"][i][1] += y
                for i in range(g_data["player"]-2):
                    if(g_data["vote"][i][0]=='B'):
                        for j in range(len(g_data["score"])):
                            if(g_data["score"][j][0]==g_data["vote"][i][1]):
                                g_data["score"][j][1] += x+1
            elif(win=="B"):
                for i in range(len(g_data["score"])):
                    if(g_data["score"][i][0]==g_data["battle"][R][1]):
                        g_data["score"][i][1] += x
                for i in range(g_data["player"]-2):
                    if(g_data["vote"][i][0]=='A'):
                        for j in range(len(g_data["score"])):
                            if(g_data["score"][j][0]==g_data["vote"][i][1]):
                                g_data["score"][j][1] += y+1
            g_data["round"] += 1
            g_data["cnt"] = 0
            g_data["vote"] = []
            g_data["pc1"] = []
            g_data["pc2"] = []
            write_file("game",g_data)
            if(x>y):
                await lobby.send("本局結果："+str(x)+"票對"+str(y)+"票，A將被火車輾過。")
            elif(y>x):
                await lobby.send("本局結果："+str(x)+"票對"+str(y)+"票，B將被火車輾過。")
            if(g_data["round"]==g_data["player"]):
                xx,yy,ww,ne = [],[],[],[]
                for i in g_data["score"]:
                    xx.append(i[0])
                for i in xx:
                    zz = []
                    for j in xx:
                        aa,bb = 0,0
                        try:
                            aa = r_data[i][0]
                        except:
                            aa = 0
                        try:
                            bb = r_data[j][0]
                        except:
                            bb = 0
                        zz.append((aa+100)/(aa+bb+200))
                    yy.append(zz)
                for i in range(len(xx)):
                    zz = []
                    for j in range(len(xx)):
                        if(g_data["score"][i][1]>=g_data["score"][j][1]):
                            zz.append(1)
                        else:
                            zz.append(0)
                    ww.append(zz)
                #print(yy)
                #print(ww)
                for i in range(len(xx)):
                    delta = 0
                    for j in range(len(xx)):
                        aa,bb = 0,0
                        try:
                            aa = r_data[xx[i]][0]
                        except:
                            aa = 0
                        try:
                            bb = r_data[xx[j]][0]
                        except:
                            bb = 0
                        if(ww[i][j]==1 and i!=j and aa<100):
                            delta += int(abs(aa-bb)*(1-yy[i][j]))+30
                        elif(ww[i][j]==1 and i!=j):
                            delta += int(abs(aa-bb)*(1-yy[i][j])*0.34764)+3
                        elif(ww[i][j]==1 and i!=j and aa>=400):
                            delta -= int(abs(aa-bb)*(1-yy[i][j])*0.13874)-1
                        elif(ww[i][j]==0 and i!=j):
                            delta -= int(abs(aa-bb)*(yy[i][j])*0.48763)-1
                    if(aa<100):
                        delta = max(delta,1)
                    ne.append(delta)
                #print(ne)
                for i in range(len(xx)):
                    try:
                        r_data[xx[i]] = [r_data[xx[i]][0]+ne[i],ne[i]]
                    except:
                        r_data[xx[i]] = [0+ne[i],ne[i]]
                write_file("train/rating",r_data)
                await lobby.send("遊戲結束")
                return
                ####
            lobby = self.bot.get_channel(997875993907834931)
            g_data = read_file("game")
            R = g_data["round"]
            z = "Round."+str(R+1)+'\n'
            z += "<@"+g_data["battle"][R][0]+"> vs. <@"+g_data["battle"][R][1]+">"
            embed = discord.Embed(title="當前比賽狀況",description=z,color=0xeee657)
            x,y = "可是：","可是："
            for i in g_data["pc1"]:
                x += " ["+i+"] "
            for i in g_data["pc2"]:
                y += " ["+i+"] "
            embed.add_field(name="A鐵軌："+str(g_data["card_info"][R][0]), value=x, inline=False)
            embed.add_field(name="B鐵軌："+str(g_data["card_info"][R][1]), value=y, inline=False)
            embed.set_footer(text=ver)
            await lobby.send(embed=embed)    
    @commands.command(aliases=["察看手牌","手牌","查看手牌","cards"],help="")
    async def my_cards(self,message):
        ID = str(message.author.id)
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        R = g_data["round"]
        if(ID==g_data["battle"][R][0]):
            embed = discord.Embed(title="您的手牌",description="總共7張，[空]代表已使用，無法再使用",color=0xeee657)
            for i in range(7):
                embed.add_field(name=str(i+1)+"號", value="["+g_data["player_info"][R][0][i]+"]", inline=False)
            embed.set_footer(text=ver)
            await message.channel.send(embed=embed)
        elif(ID==g_data["battle"][R][1]):
            embed = discord.Embed(title="您的手牌",description="總共7張，[空]代表已使用，無法再使用",color=0xeee657)
            for i in range(7):
                embed.add_field(name=str(i+1)+"號", value="["+g_data["player_info"][R][1][i]+"]", inline=False)
            embed.set_footer(text=ver)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("現在不是您的回合，沒有手牌可以看喔！")
    @commands.command(aliases=["察看角色","角色","查看角色","characters"],help="")
    async def my_characters(self,message):
        ID = str(message.author.id)
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        R = g_data["round"]
        if(ID==g_data["battle"][R][0]):
            embed = discord.Embed(title="您的角色",description="總共3張，只能選定一張做為保護對象，選了之後不能更改。",color=0xeee657)
            for i in range(3):
                embed.add_field(name=str(i+1)+"號", value="["+g_data["card_choose"][R][0][i]+"]", inline=False)
            embed.set_footer(text=ver)
            await message.channel.send(embed=embed)
        elif(ID==g_data["battle"][R][1]):
            embed = discord.Embed(title="您的角色",description="總共3張，只能選定一張做為保護對象，選了之後不能更改。",color=0xeee657)
            for i in range(3):
                embed.add_field(name=str(i+1)+"號", value="["+g_data["card_choose"][R][1][i]+"]", inline=False)
            embed.set_footer(text=ver)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("現在不是您的回合，沒有手牌可以看喔！")
    @commands.command(aliases=["出牌","use"],help="")
    async def use_card(self,message,num:int,who:str):
        ID = str(message.author.id)
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        R = g_data["round"]
        if(num<=0 or num>7):
            await message.channel.send("選擇的手牌必須為1~7號")
            return
        num -= 1
        if(who!='A' and who!='B'):
            await message.channel.send("選擇出牌對象只能是A或B。")
            return
        if(g_data["card_info"][R][0]=="待選擇" or g_data["card_info"][R][1]=="待選擇"):
            await message.channel.send("待所有玩家都選完保護對象後才能出牌。")
            return
        if(ID==g_data["battle"][R][0]):
            if(g_data["cnt"]%2!=0 or g_data["cnt"]>=6):
                await message.channel.send("沒有輪到你出牌！")
                return
            if(g_data["player_info"][R][0][num]!="無"):
                if(who=='A'):
                    g_data["pc1"].append(g_data["player_info"][R][0][num])
                    g_data["player_info"][R][0][num] = "無"
                elif(who=='B'):
                    g_data["pc2"].append(g_data["player_info"][R][0][num])
                    g_data["player_info"][R][0][num] = "無"
                g_data["cnt"] += 1
                write_file("game",g_data)
                await message.channel.send("出牌成功。")
                z = "Round."+str(R+1)+'\n'
                z += "<@"+g_data["battle"][R][0]+"> vs. <@"+g_data["battle"][R][1]+">"
                embed = discord.Embed(title="當前比賽狀況",description=z,color=0xeee657)
                x,y = "可是：","可是："
                for i in g_data["pc1"]:
                    x += " ["+i+"] "
                for i in g_data["pc2"]:
                    y += " ["+i+"] "
                embed.add_field(name="A鐵軌："+str(g_data["card_info"][R][0]), value=x, inline=False)
                embed.add_field(name="B鐵軌："+str(g_data["card_info"][R][1]), value=y, inline=False)
                embed.set_footer(text=ver)
                await lobby.send(embed=embed)
            else:
                await message.channel.send("此牌已經使用，無法出牌。")
                return
        elif(ID==g_data["battle"][R][1]):
            if(g_data["cnt"]%2!=1 or g_data["cnt"]>=6):
                await message.channel.send("沒有輪到你出牌！")
                return
            if(g_data["player_info"][R][1][num]!="無"):
                if(who=='A'):
                    g_data["pc1"].append(g_data["player_info"][R][1][num])
                    g_data["player_info"][R][1][num] = "無"
                elif(who=='B'):
                    g_data["pc2"].append(g_data["player_info"][R][1][num])
                    g_data["player_info"][R][1][num] = "無"
                g_data["cnt"] += 1
                write_file("game",g_data)
                await message.channel.send("出牌成功。")
                z = "Round."+str(R+1)+'\n'
                z += "<@"+g_data["battle"][R][0]+"> vs. <@"+g_data["battle"][R][1]+">"
                embed = discord.Embed(title="當前比賽狀況",description=z,color=0xeee657)
                x,y = "可是：","可是："
                for i in g_data["pc1"]:
                    x += " ["+i+"] "
                for i in g_data["pc2"]:
                    y += " ["+i+"] "
                embed.add_field(name="A鐵軌："+str(g_data["card_info"][R][0]), value=x, inline=False)
                embed.add_field(name="B鐵軌："+str(g_data["card_info"][R][1]), value=y, inline=False)
                embed.set_footer(text=ver)
                await lobby.send(embed=embed)
            else:
                await message.channel.send("此牌已經使用，無法出牌。")
                return
        else:
            await message.channel.send("現在不是您的回合，無法出牌！")
            return
        
    @commands.command(aliases=["保護","protect"],help="")
    async def protect_character(self,message,num:int):
        ID = str(message.author.id)
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        R = g_data["round"]
        if(num<=0 or num>3):
            await message.channel.send("選擇的手牌必須為1~3號。")
            return
        num -= 1
        if(ID==g_data["battle"][R][0]):
            if(g_data["card_info"][R][0]!="待選擇"):
                await message.channel.send("您已經選擇完保護對象了。")
                return
            g_data["card_info"][R][0] = g_data["card_choose"][R][0][num]
            write_file("game",g_data)
            await message.channel.send("選擇成功。")
            await lobby.send("<@"+ID+">已選擇保護對象。")
        elif(ID==g_data["battle"][R][1]):
            if(g_data["card_info"][R][1]!="待選擇"):
                await message.channel.send("您已經選擇完保護對象了。")
                return
            g_data["card_info"][R][1] = g_data["card_choose"][R][1][num]
            write_file("game",g_data)
            await message.channel.send("選擇成功。")
            await lobby.send("<@"+ID+">已選擇保護對象。")
        else:
            await message.channel.send("現在不是您的回合，無法出牌！")
    @commands.command(aliases=["分數","得分","記分板"],help="")
    async def score(self,message):
        ID = str(message.author.id)
        lobby = self.bot.get_channel(997875993907834931)
        g_data = read_file("game")
        x = []
        for i in g_data["score"]:
            x.append([-i[1],i[0]])
        x = sorted(x)
        embed = discord.Embed(title="記分板",description="沒什麼用的記分板hehe",color=0xeee657)
        add = ""
        la = 1
        las = 8787878787
        for i in range(len(x)):
            if(-x[i][0]==-las):
                add += "No."+str(la)+":<@"+x[i][1]+">:"+str(-x[i][0])+"\n"
            else:
                la = i+1
                add += "No."+str(i+1)+":<@"+x[i][1]+">:"+str(-x[i][0])+"\n"
            las = x[i][0]

        embed.add_field(name="分數", value=add, inline=False)
        embed.set_footer(text=ver)
        await lobby.send(embed=embed)
            

   
def setup(bot):
  bot.add_cog(Train(bot))

#NzczNTYwNTQ3NDQ1OTY0ODgx.X6LAZg.gY0VE7ne5RNnML1JEbeMo3MkCqM
