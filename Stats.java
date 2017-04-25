package it.moondroid.coverflowdemo;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

import java.util.ArrayList;

import it.moondroid.coverflow.components.ui.containers.FeatureCoverFlow;

public class Stats extends ActionBarActivity {
    public String team, games_played, wins, losses, rank, points, streak;
    //public String[] teams = getResources().getStringArray(R.array.teams);
    //public String[] team_abbreviations = getResources().getStringArray(R.array.teams);
    private String games_played_query, wins_query, losses_query, overtime_losses_query, rank_query, points_query, streak_query;

    private FeatureCoverFlow mCoverFlow;
    private CoverFlowAdapter mAdapter;
    private ArrayList<GameEntity> mData = new ArrayList<>(0);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_stats);

        Bundle bundle = getIntent().getExtras();
        team = bundle.getString("team");
        games_played = bundle.getString("games_played");
        wins = bundle.getString("wins");
        losses = bundle.getString("losses");
        rank = bundle.getString("rank");
        points = bundle.getString("points");
        streak = bundle.getString("streak");

        final TextView team_name = (TextView) findViewById(R.id.team_name);
        team_name.setText(team);

        final TextView gp = (TextView) findViewById(R.id.gp);
        gp.setText(games_played);

        final TextView w = (TextView) findViewById(R.id.w);
        w.setText(wins);

        final TextView l_otl = (TextView) findViewById(R.id.l_otl);
        l_otl.setText(losses);

        final TextView rnk = (TextView) findViewById(R.id.rnk);
        rnk.setText(rank);

        final TextView p = (TextView) findViewById(R.id.p);
        p.setText(points);

        final TextView strk = (TextView) findViewById(R.id.strk);
        strk.setText(streak);


        mData.add(new GameEntity(R.string.team1_name, R.mipmap.ducks, R.string.team2_name, R.mipmap.predators));
        mData.add(new GameEntity(R.string.team1_name, R.mipmap.ducks, R.string.team2_name, R.mipmap.predators));
        mData.add(new GameEntity(R.string.team1_name, R.mipmap.ducks, R.string.team2_name, R.mipmap.predators));
        mData.add(new GameEntity(R.string.team1_name, R.mipmap.ducks, R.string.team2_name, R.mipmap.predators));

        mAdapter = new CoverFlowAdapter(this);
        mAdapter.setData(mData);
        mCoverFlow = (FeatureCoverFlow) findViewById(R.id.coverflow);
        mCoverFlow.setAdapter(mAdapter);

    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_coverflow_activity, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

}
