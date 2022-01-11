class Schedule(TypedDict):
    time: str
    location: str


class VillagerSchedules(Model):
    brief: List[str]
    schedule: List[
        Tuple[str, List[Tuple[Union[str, None], List[Schedule]]]]
    ]  # [( requirement, [( condition, [schedules] )] )]

    def __init__(
        self,
        brief: List[str],
        schedule: Dict[str, List[Tuple[Union[str, None], List[Schedule]]]],
    ):
        self.brief = brief
        self.schedule = schedule

    @classmethod
    def parse(cls, page: BeautifulSoup):
        schedules_heading = page.find(id="Schedule")
        if schedules_heading is None:
            return None

        briefs_p = schedules_heading.find_all_next()
        is_special = briefs_p[0].name == "h3"

        brief = []
        if not is_special:
            for p in briefs_p:
                if p.name != "p":
                    if len(brief) > 0 or p.name == "h2":
                        break
                else:
                    if len((desc := strip_text(p))) > 1:
                        brief += [desc]

        schedule_tables = schedules_heading.find_all_next(["table", "h2"])

        schedules = {"requirement": None, "schedules": []}
        vschedule = []
        for sched_elm in schedule_tables:
            if sched_elm.name == "h2":
                vschedule += [(schedules["requirement"], schedules["schedules"])]
                break
            if sched_elm.name == "table":
                if (c_ := sched_elm.get("class")) and "wikitable" in c_:
                    if not is_special:
                        condition = (
                            strip_text(c)
                            if (
                                c := sched_elm.find_previous_siblings(["p", "h2"])[0]
                            ).name
                            == "p"
                            else strip_text(sched_elm.find_next("th"))
                        )
                        requirement = (
                            strip_text(r)
                            if not (r := sched_elm.find_previous("span")).get("class")
                            else None
                        )
                    else:
                        condition = strip_text(sched_elm.find_next("th"))
                        requirement = (
                            strip_text(r)
                            if (r := sched_elm.find_previous("h3"))
                            else None
                        )

                    rows = sched_elm.find_all("tr")[1:]
                    schedule = [
                        Schedule(time=col[0], location=col[1])
                        for col in [
                            (strip_text(cols[0]), strip_text(cols[1]))
                            for cols in [row.find_all("td") for row in rows]
                        ]
                    ]
                    schedules["requirement"] = requirement
                    schedules["schedules"] += [(condition, schedule)]
                else:
                    if len(schedules["schedules"]):
                        vschedule += [
                            (schedules["requirement"], schedules["schedules"])
                        ]
                        schedules["schedules"] = []

                    is_special = False

        return cls(brief=brief, schedule=vschedule)
