public static TimeSpan HandleTime(string input)
        {
            var match = Regex.Match(input, @"^(?=\d)((?<hours>\d+)h)?\s*((?<minutes>\d+)m?)?$", RegexOptions.ExplicitCapture);
            if (match.Success)
            {
                int hours;
                int.TryParse(match.Groups["hours"].Value, out hours);

                int minutes;
                int.TryParse(match.Groups["minutes"].Value, out minutes);

                return new TimeSpan(0, hours, minutes, 0);
            }
            return new TimeSpan(0, 0, 0, 0);
        }

[Group("afk"),Alias("brb"), Name("Away From Keyboard")]
        public class SubModule2 : ModuleBase<SocketCommandContext>
        {
            [Command]
            [Remarks("Sets you afk, or back")]
            public async Task Away([Summary("Time and/or Reason")][Remainder]string reason = null)
            {
                using (var db = new NeoContext())
                {
                    if(db.Afks.Any(afk => afk.User == db.Users.FirstOrDefault(u => u.Id == Context.User.Id))) //user is afk so he is back now
                    {
                        var obj = db.Afks.FirstOrDefault(afk => afk.User == db.Users.FirstOrDefault(u => u.Id == Context.User.Id));
                        if(string.IsNullOrEmpty(obj.Reason))
                        {
                            var embed = NeoEmbeds.Afk($"{Context.User} is back!", Context.User);
                            await ReplyAsync("", false, embed.Build());
                        }
                        else
                        {
                            var embed = NeoEmbeds.Afk($"{Context.User} is back from {obj.Reason.TrimStart()}!", Context.User);
                            await ReplyAsync("", false, embed.Build());
                        }
                        db.Afks.Attach(obj);
                        db.Afks.Remove(obj);
                        db.SaveChanges();
                    }
                    else
                    {
                        var obj = new Afk();
                        if (reason != null) // there is time and or reason
                        {
                            var time = reason.Substring(0, reason.IndexOf(' ') <= -1 ? reason.Length : reason.IndexOf(' ')); // get first block
                            if (CheckTimeString(time))//check if first block is time string
                            {
                                TimeSpan timestr = HandleTime(time); //get timespan from that block
                                reason = reason.Replace(time, "");//get time out of reason
                                if (reason.Length == 0)
                                {
                                    var embed = NeoEmbeds.Afk($"{Context.User} is now afk!", Context.User, null, Thing(timestr));
                                    await ReplyAsync("", false, embed.Build());
                                    obj.Reason = null;
                                    obj.Time = (DateTime.Now + timestr);
                                    obj.User = db.Users.FirstOrDefault(u => u.Id == Context.User.Id);
                                }
                                else
                                {
                                    var embed = NeoEmbeds.Afk($"{Context.User} is now afk!", Context.User, reason, Thing(timestr));
                                    await ReplyAsync("", false, embed.Build());
                                    obj.Reason = reason;
                                    obj.Time = (DateTime.Now + timestr);
                                    obj.User = db.Users.FirstOrDefault(u => u.Id == Context.User.Id);
                                }

                            }
                            else//no time just reason
                            {
                                var embed = NeoEmbeds.Afk($"{Context.User} is now afk!", Context.User, reason);
                                await ReplyAsync("", false, embed.Build());
                                obj.Reason = reason;
                                obj.Time = default(DateTime);
                                obj.User = db.Users.FirstOrDefault(u => u.Id == Context.User.Id);
                            }
                        }
                        else//no reason and time
                        {
                            var embed = NeoEmbeds.Afk($"{Context.User} is now afk!", Context.User);
                            await ReplyAsync("", false, embed.Build());
                            obj.Reason = null;
                            obj.Time = default(DateTime);
                            obj.User = db.Users.FirstOrDefault(u => u.Id == Context.User.Id);
                        }
                        db.Afks.Add(obj);
                        db.SaveChanges();
                    }
                }
            }
        }