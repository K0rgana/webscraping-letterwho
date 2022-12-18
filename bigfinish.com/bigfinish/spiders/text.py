ranges_hub = [
    'ranges/v/torchwood',
    'ranges/v/torchwood-special-releases',
    'ranges/v/torchwood-the-story-continues',
    'ranges/v/torchwood-one',
    'ranges/v/torchwood-soho',
    'ranges/v/unit',
    'ranges/v/unit---the-new-series',
    'ranges/v/the-worlds-of-doctor-who---special-releases',
    'ranges/v/doctor-who-the-new-adventures-of-bernice-summerfield',
    'ranges/v/bernice-summerfield',
    'ranges/v/bernice-summerfield-books',
    'ranges/v/charlotte-pollard',
    'ranges/v/iris-wildthyme',
    'ranges/v/iris-wildthyme-and-friends',
    'ranges/v/river-song',
    'ranges/v/sarah-jane-smith',
    'ranges/v/the-lives-of-captain-jack',
    'ranges/v/jago-litefoot',
    'ranges/v/the-paternoster-gang',
    'ranges/v/counter-measures',
    'ranges/v/class',
    'ranges/v/the-robots',
    'ranges/v/missy',
    'ranges/v/the-war-master',
    'ranges/v/gallifrey',
    'ranges/v/cyberman',
    'ranges/v/dalek-empire',
    'ranges/v/i-davros',
    'ranges/v/doctor-who---the-first-doctor-adventures',
    'ranges/v/doctor-who-the-second-doctor-adventures',
    'ranges/v/doctor-who---the-third-doctor-adventures',
    'ranges/v/doctor-who---fourth-doctor-adventures',
    'ranges/v/doctor-who---the-fifth-doctor-adventures',
    'ranges/v/doctor-who---the-sixth-doctor-adventures',
    'ranges/v/doctor-who---the-seventh-doctor-adventures',
    'ranges/v/eighth-doctor-adventures',
    'ranges/v/doctor-who---the-war-doctor',
    'ranges/v/doctor-who-the-ninth-doctor-adventures',
    'ranges/v/doctor-who---the-tenth-doctor-adventures',
    'ranges/v/monthly-series',
    'ranges/v/doctor-who-the-audio-novels',
    'ranges/v/doctor-who---companion-chronicles',
    'ranges/v/doctor-who---the-early-adventures1',
    'ranges/v/doctor-who---the-lost-stories',
    'ranges/v/doctor-who---short-trips',
    'ranges/v/doctor-who---short-trips-rareties',
    'ranges/v/doctor-who---the-doctor-chronicles',
    'ranges/v/doctor-who---unbound',
    'ranges/v/doctor-who-time-lord-victorious',
    'ranges/v/doctor-who-once-and-future',
    'ranges/v/doctor-who-destiny-of-the-doctors',
    'ranges/v/doctor-who---novel-adaptations',
    'ranges/v/doctor-who---classic-series---special-releases',
    'ranges/v/doctor-who-philip-hinchcliffe-presents',
    'ranges/v/doctor-who-auf-deutsch',
    'ranges/v/doctor-who---the-stage-plays',
]

u_range= ranges_hub[31]
u_page = "/page:{}"
u_base = 'https://www.bigfinish.com'
u_filter_asc = f"?url={u_range}&sort_ordering=date_asc"
u_filter_des = f"?url={u_range}&sort_ordering=date_des"
url = f"{u_base}/{u_range}{u_page.format(1)}{u_filter_asc}"
last_url = f"{u_base}/{u_range}{u_page.format(1)}{u_filter_des}"

print(u_range)
print(url)
print(last_url)