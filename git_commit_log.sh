echo "Github commits in 2020" > git_commit_logs.txt
echo -n "Jan : " >> git_commit_logs.txt
git rev-list --count --since="Jan 1 2020"  --before="Feb 1 2020" --all >> git_commit_logs.txt
echo -n "Feb : " >> git_commit_logs.txt
git rev-list --count --since="Feb 1 2020"  --before="Mar 1 2020" --all >> git_commit_logs.txt
echo -n "Mar : " >> git_commit_logs.txt
git rev-list --count --since="Mar 1 2020"  --before="Apr 1 2020" --all >> git_commit_logs.txt
echo -n "Apr : " >> git_commit_logs.txt
git rev-list --count --since="Apr 1 2020"  --before="May 1 2020" --all >> git_commit_logs.txt
echo -n "May : " >> git_commit_logs.txt
git rev-list --count --since="May 1 2020"  --before="Jun 1 2020" --all >> git_commit_logs.txt
echo -n "Jun : " >> git_commit_logs.txt
git rev-list --count --since="Jun 1 2020"  --before="Jul 1 2020" --all >> git_commit_logs.txt
echo -n "Jul : " >> git_commit_logs.txt
git rev-list --count --since="Jul 1 2020"  --before="Aug 1 2020" --all >> git_commit_logs.txt
echo -n "Total : " >> git_commit_logs.txt
git rev-list --count --since="Jan 1 2020"  --before="Aug 1 2020" --all >> git_commit_logs.txt