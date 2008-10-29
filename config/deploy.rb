set :application, "rttvsocial"

set :deploy_to, "/home/ike/#{application}"
set :scm, :bzr
set :checkout, "branch"
set :repository, "/home/ike/dev/#{application}"
set :user, "ike"
#set :password, "erhgeh573w"
set :password, "irapupa1988"
role :app, "208.101.30.17"

namespace :deploy do
  task :fast_restart, :roles => :app do
    run "cd ~/run/ && kill `cat /home/ike/run/#{application}.pid`"
    run "cd ~/#{application}/ && python2.5 manage.py runfcgi method=prefork host=127.0.0.1  port=3034 pidfile=/home/ike/run/#{application}.pid"
  end
  task :fast_stop, :roles => :app do
     run "cd ~/run/ && kill `cat /home/ike/run/#{application}.pid`"
  end
  
  task :fast_start, :roles => :app do
    run "cd ~/#{application}/ && python2.5 manage.py runfcgi method=prefork host=127.0.0.1 port=3034 pidfile=/home/ike/run/#{application}.pid"
  end
  
  task :deploy_app, :roles => :app do
      `bzr push sftp://ike@208.101.30.17/home/ike/#{application}`
      run "cd /home/ike/#{application} && bzr checkout"
  end
  
  task :update_local, :roles => :app do
      `bzr pull sftp://ike@208.101.30.17/home/ike/#{application}`
      `bzr update`  
  end

  task :hot_update, :roles => :app do     	
	  `bzr push sftp://ike@208.101.30.17/home/ike/#{application}`
	  run "cd /home/ike/#{application} && bzr update"
	  run "cd ~/run/ && kill `cat #{application}.pid`"
    run "cd ~/#{application}/ && python2.5 manage.py runfcgi method=prefork host=127.0.0.1 port=3034 pidfile=/home/ike/run/#{application}.pid"      
  end
  
  task :checkout, roles => :app do
    `bzr pull sftp://ike@208.101.30.17/home/ike/#{application}`
    `bzr checkout`
  end
end