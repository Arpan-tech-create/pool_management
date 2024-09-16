const vm=new Vue({
    el: '#app',
    delimiters: ["${", "}"],
    data: {
      chartOptions: {
        chart: {
          type: 'column'
        },
        title: {
          text: 'Pool Capacity, Used Space, and Free Space'
        },
        xAxis: {
          categories: [], 
          title: {
            text: ''
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: 'Space (GB)'
          },
          labels: {
            formatter: function() {
                return this.value + ' GB';
            }
          },
          stackLabels: {
            enabled: false,
          }
        },
        legend: {
          align: 'left',
          x: 100,
          verticalAlign: 'top',
          y: 70,
          floating: true,
          backgroundColor: 'white',
          borderWidth: 1
        },
        credits: {
          enabled: false
        },
        plotOptions: {
          column: {
            stacking: 'normal',
            dataLabels: {
              enabled: true,
              rotation: 0,
              inside: true,
              verticalAlign: 'middle',
              y: 0,
              style: {
                fontWeight: 'bold',
                fontSize: '14px',
              }
            },
            // Add click event for pool chart columns
            point: {
              events: {
                click: function(event){
                    console.log("Event context:", this); // Debug the context
                    console.log("Vue instance:", window.vm); // Verify Vue instance
                    window.vm.fetchSlaveData(event); 
                } // Handle click to fetch slave data
              }
            }
          }
        },
        series: [
          {
            name: 'Capacity',
            data: [] 
          },
          {
            name: 'Used Space',
            data: [] 
          },
          {
            name: 'Free Space',
            data: [] 
          }
        ]
      },
      slaveChartOptions: {
        chart: {
          type: 'column'
        },
        title: {
          text: 'Slave Disks Capacity and Free Space'
        },
        xAxis: {
          categories: [],
          title: {
            text: ''
          }
        },
        yAxis: {
          min: 0,
          title: {
            text: 'Space (GB)'
          },
          labels: {
            formatter: function() {
              return this.value + ' GB';
            }
          },
          stackLabels: {
            enabled: false
          }
        },
        legend: {
          align: 'left',
          x: 100,
          verticalAlign: 'top',
          y: 70,
          floating: true,
          backgroundColor: 'white',
          borderWidth: 1
        },
        credits: {
          enabled: false
        },
        plotOptions: {
          column: {
            stacking: 'normal',
            dataLabels: {
              enabled: true,
              rotation: 0,
              inside: true,
              verticalAlign: 'middle',
              y: 0,
              style: {
                fontWeight: 'bold',
                fontSize: '14px'
              }
            }
          }
        },
        
        series: [
          {
            name: 'Capacity',
            data: []
          },
          {
name:'Usage',
data:[]
          },
          {
            name: 'Free Space',
            data: []
          }
        ],
        noData: {
          // Message displayed when there's no data
          style: {
            fontWeight: 'bold',
            fontSize: '16px',
            color: '#303030'
          },
          position: {
            align: 'center',
            verticalAlign: 'middle'
          }
        }
      },
      disk_count: 0,
      pool_count: 0,
      showSlaveChart: false, // Initially hide the slave chart
    },
    mounted() {
      this.fetchPoolData();
     
    },
    methods: {
      fetchPoolData() {
        fetch('/pool_data')
          .then(response => response.json())
          .then(data => {
            const poolNames = data.map(pool => pool.pool_name);
            const capacities = data.map(pool => parseInt(pool.capacity));
            const usedSpaces = data.map(pool => parseInt(pool.used_space));
            const freeSpaces = data.map(pool => parseInt(pool.free_space));
  
            this.chartOptions.xAxis.categories = poolNames;
            this.chartOptions.series[0].data = capacities;
            this.chartOptions.series[1].data = usedSpaces;
            this.chartOptions.series[2].data = freeSpaces;
  
            Highcharts.chart('container', this.chartOptions);
          })
          .catch(error => console.error('Error fetching pool data:', error));
      },
      fetchSlaveData(event) {
        const poolName = event.point.category; // Get clicked pool name
        console.log("Fetching slave data for pool:", poolName); // Debug log
        this.showSlaveChart = true;
        fetch(`/slave_data?pool_name=${poolName}`)
          .then(response => response.json())
          .then(data => {
            console.log("Slave data fetched:", data); // Debug log
            const diskNames = data.map(disk => disk.disk_name);
            const capacities = data.map(disk => parseInt(disk.capacity));
            const usage=data.map(disk=>parseInt(disk.usage));
            const freeSpaces = data.map(disk => parseInt(disk.free_space));
        this.slaveChartOptions.title.text = `Slave Disks Capacity and Free Space for ${poolName}`;
  
            // Update slave chart options with the new data
            this.slaveChartOptions.xAxis.categories = diskNames;
            this.slaveChartOptions.series[0].data = capacities;
            this.slaveChartOptions.series[1].data=usage
            this.slaveChartOptions.series[2].data = freeSpaces;
      
            // Show the slave chart and render it
      
            if (data.length === 0) {
              Highcharts.chart('slave-chart', this.slaveChartOptions).showNoData();
            } else {
              Highcharts.chart('slave-chart', this.slaveChartOptions);
            }
          })
          .catch(error => console.error('Error fetching slave data:', error));
      }
      
    }
  });
  

window.vm = vm;