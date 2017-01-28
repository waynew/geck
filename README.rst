GECK: Garden of Eden Creation Kit
=================================

This world may not be perfect, but GECK strives to provide you with your own
little Garden of Eden.

----

GECK was born from my frustration with existing build tools. Out of the two
main free build tools that I've found you have Jenkins and Buildbot. Jenkins
frustrated me because it was difficult to manage via SaltStack. The lack of
plain-text configuration files just didn't sit well with me.

Buildbot was a fairly decent answer to that - but the UI was trying too hard to
be flashy, requiring coffescript and was in general pretty weird and not very
hackable. If you wanted to do something extra you needed to learn an entirely
new toolset. Ick. And the back end API was a little awkward. It didn't adhere
to pep8 at all, and the default was not really to do the right thing. It took
me a lot of work to actually figure out how to configure the darn thing. But it
was better than Jenkins. Until the UI totally stopped working for me.

So I built GECK with the following ideas:

- it should be easy to do normal things
- it should be easy to extend to work with the way you want to work
- it should integrate with the tools that you already have


Normal Things
-------------

What does normal even mean? Well for starters, I figure that 90-99% of the time
the reason you're going to be building software is in response to pushing a
commit to a (D)VCS. And in particular you're *probably* going to be pushing to
GitHub, cause that's what all the rest of the cool kids are doing. If you're
not pushing to GitHub then you're probably pushing to GitLab or BitBucket or
Kiln or something. These services all provide webhook capabilities, but in the
off chance that you don't want *that* feature then it should be super easy to
poll for changes.

🎶 Ch-Ch-Ch-Ch-Chaanges 🎶
**************************

Getting changes is as easy as one of the following:

::

    project = geck.Project('Introduction')
    project.add_webhook('github', TODO some stuff github provides)
    project.add_webhook('bitbucket', TODO more info)
    project.add_webhook('gitlab', TODO more info)
    project.add_webhook('kiln', TODO more info)


Or if you're into polling instead:

::

    project.git_poll('git@github.com:waynew/geck.git')
    project.hg_poll('ssh://hg@bitbucket.org/waynew/project')
    project.svn_poll('http://svn.apache.org/repos/asf/bugs/')

I have no idea why you'd want to use SVN, but it's there if you need it. Don't
see your `favorite VCS <http://darcs.net/>`_? We welcome pull requests!

You might even be weird and just want to do stuff locally. That's OK, we've got
you covered with that, too. Well, that's really just because your VCS is that
good. Anyway:

::

    project.git_poll('/path/to/your/repo')

That'll work just fine!

Oh, and maybe you want to check a bunch of different endpoints. You can do
that, too:

::

    project.add_poller('git@github.com:waynew/geck.git')
    project.add_poller('/home/wayne/programming/geck')

Any of these things should Just Work™.

Building Stuff
**************

So you can be notified or pull changes in... now what? Well, that's where the
build steps come in. Most people are probably going to want to either be
building a package of some sort or running some tests - or both! It will be
super nice when we have support for building all of the things, but since this
*is* a Python package you should not be surprised that the first supported
feature is going to be running Python tests and building Python wheels:

::

    project.add_step(geck.py.spinx('geck', output='/var/www/geck'))
    project.add_step(geck.util.tasks_scan())
    project.add_step(geck.py.pylint())
    project.add_step(geck.py.run_pytest(tests='tests', cov='geck',
    junitxml='build/tests.xml')
    project.add_step(geck.py.build_wheel())
    project.add_step(geck.github.create_release('{version}'))
    project.add_step(geck.util.upload_file('build/{version}.whl',
    'http://uploads.github.com/repos/wayne/geck/releases/{version}/assets?name={filename}'))

Yeah, that's right. You just released your software in like 10 lines. Even
better? You don't even have to upload the file that way, you could just do
this:

::

    project.add_step(geck.github.release_asset('/build/{version}.whl'))

Not Python? No Problem!
***********************

Support may not *yet* be as nice for your language, but don't worry, you can
still build stuff:

::

    project.add_step(geck.cmd.run(['gcc', 'project.c', '-o', 'fuzz']))
    project.add_step(geck.cmd.run('build/fuzz hello', pass_on=[0,1],
    warn_on=[2,3]))

And if you want some nicer support for your language, we're accepting pull
requests!

Notifications
*************

Surely you don't care when things break, do you? Oh, you do! Well, good thing
we've got support for that.

::

    project.add_notifier(geck.slack.notifier('https://hooks.slack.com/services/ABC123/ABC123/AbcD123476789'))

Or if you wanted to roll your own, you could do that, too:

::

    project.add_notifier(geck.web.notifier(
        url='https://example.com/status',
        method='POST',
        message='build {name} {action} because {reason}',
        on=geck.Status.build_start | geck.Status.build_end,
    ))


I Don't Like Python
*******************

That's cool. You don't have to write Python to use GECK. You can pretend that
it's not Python under the covers, I don't judge (okay maybe a little). Just
write your config like this:

::

    {'project':
        {'name': 'Geck',
         'pollers': {'git': 'git@github.com:waynew/geck.git',
                     'hg': 'ssh://hg@bitbucket.org/waynew/project'},
         'steps': [
            {'geck.py.sphinx': {'package': 'geck', 'output': '/var/www/geck'}},
            'geck.util.tasks_scan',
            'geck.py.pylint',
            {'geck.py.run_pytest': {'tests': 'tests', 'cov': 'geck',
                                    'junitxml': 'build/tests.xml'}},
            'geck.py.build_wheel',
            {'geck.github.create_release': {'version': '{version}'}},
            {'geck.github.release_asset': {'filename': '/build/{version}.whl'}}
         ],
         'notifiers': [
            {'geck.slack.notifier': {'url': 'https://hooks.slack.com/services/ABC123/ABC123/AbcD123476789'}}
         ]}
    }

Then stick it in ``projects/geck.json`` and you're all set.

Roadmap
*******

Currently, no code exists. Here are the features that I have planned, roughly
in order of the priority that I want to work on them:

* Linux/Mac support
* git polling
* building in response to git polling
* publishing build results (static HTML please)
* event broadcasting
* notifications
* scan for TODO comments
* python build tools

  * gen sphinx docs
  * run tox
  * build sdists
  * build wheels
  * run linter

* JSON/Toml/Yaml config support
* docker build tools

  * build dockerfile
* mercurial polling
* svn polling
* Windows Support


I Love This!
************

Sweet! You can `Say Thanks! <https://saythanks.io/to/waynew>`_
