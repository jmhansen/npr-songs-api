from interludes.database import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())


class Program(BaseModel):
    """ Name of the NPR program or show"""
    name = db.Column(db.String(60), unique=True, nullable=False)
    slug = db.Column(db.String(60), unique=True, nullable=False)  # TODO: figure out how to make slug
    href = db.Column(db.String(255))  # TODO: figure out href validation on field
    episodes = db.relationship('Episode', backref='program', lazy=True)

    # name = models.CharField(max_length=50, unique=True)  # maybe make a choice field
    # slug = models.SlugField(max_length=75)
    # href = models.URLField(blank=True)

    def __str__(self):
        return self.name

    # @property
    # def date_latest_episode(self):
    #     return self.episodes.latest().date
    #
    # @property
    # def date_earliest_episode(self):
    #     return self.episodes.earliest().date
    #
    # @property
    # def num_episodes(self):
    #     return self.episodes.count()
    #
    # @property
    # def num_interludes(self):
    #     return Interlude.objects.filter(episode__program=self).count()


class Episode(BaseModel):
    """ Specific airing of a program, unique by date"""
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
    date = db.Column(db.Date)
    interludes = db.relationship('Interlude', backref='episode', lazy=True)

    # class Meta:
    #     unique_together = ('program', 'date')
    #     get_latest_by = 'date'


class Artist(BaseModel):
    name = db.Column(db.String(125), unique=True)
    slug = db.Column(db.String(150), unique=True)
    thumbnail = db.Column(db.String(255))
    # for 'Various Artists', 'NA', and others that should not be displayed in lists of artists
    hidden = db.Column(db.Boolean, default=False)
    songs = db.relationship('Song', backref='artist', lazy=True)

    def __str__(self):
        return self.name

    # @property
    # def num_songs(self):
    #     return self.songs.count()
    #
    # @property
    # def num_interludes(self):
    #     return Interlude.objects.filter(song__artist=self).count()
    #
    # @property
    # def earliest_episode(self):
    #     return Episode.objects.filter(interludes__song__artist=self).earliest('date')
    #
    # @property
    # def latest_episode(self):
    #     return Episode.objects.filter(interludes__song__artist=self).latest('date')


class Song(BaseModel):
    name = db.Column(db.String(125))
    # Some songs do not have an artist listed (maybe create a 'None' artist?)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=True)
    preview = db.Column(db.String(255))
    hidden = db.Column(db.Boolean, default=False)
    interludes = db.relationship('Interlude', backref='song', lazy=True)

    class Meta:
        unique_together = ('name', 'artist')

    def __str__(self):
        return self.name

    # @property
    # def num_interludes(self):
    #     return self.interludes.count()
    #
    # @property
    # def date_last_played(self):
    #     return self.interludes.latest().episode.date


class Interlude(BaseModel):
    """ The clip or instance of a song used in an interlude. """
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    order = db.Column(db.Integer)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'))

    # class Meta:
    #     unique_together = ('song', 'order', 'episode')
    #     get_latest_by = 'episode__date'
    #     ordering = ['order']

    def __str__(self):
        return "{} - {} - {}".format(self.song.name, self.episode.program.name, self.order)
